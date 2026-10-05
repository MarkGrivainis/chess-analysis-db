from datetime import datetime

import chess.engine
import chess.pgn

from chess_db.schemas.chess import ChessGameSchema, ChessMoveSchema


def parse_game(game: chess.pgn.Game) -> ChessGameSchema:
    engine_stockfish = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

    headers_dict = game.headers
    game_url = headers_dict.get("Link", "Unknown")
    white = headers_dict.get("White", "Unknown")
    black = headers_dict.get("Black", "Unknown")
    date = headers_dict.get("Date", "Unknown")
    eco_url = headers_dict.get("ECOUrl", "Unknown")

    board = game.board()
    parsed_moves = []
    move_number = 1

    # Traverse nodes to read internal move comments (where clock data lives)
    node = game

    last_white_clock = None
    last_black_clock = None
    while not node.is_end():
        # Get the next sequential node in the mainline
        next_node = node.variation(0)
        move = next_node.move
        turn = "White" if board.turn == chess.WHITE else "Black"

        # 1. Parse clock time out of the comment attached to this move node
        comment = next_node.comment
        clock_time = None
        time_spent = None

        if "[%clk" in comment:
            try:
                clock_time = comment.split("[%clk ")[1].split("]")[0]

                # Convert clock string (H:MM:SS.ms) into total seconds
                fmt = "%H:%M:%S.%f" if "." in clock_time else "%H:%M:%S"
                current_seconds = datetime.strptime(clock_time, fmt).time()
                total_current_seconds = (
                    current_seconds.hour * 3600
                    + current_seconds.minute * 60
                    + current_seconds.second
                    + current_seconds.microsecond / 1000000
                )

                # Calculate difference from the player's PREVIOUS move
                prior_clock = last_white_clock if turn == "White" else last_black_clock

                if prior_clock is not None:
                    time_spent = round(prior_clock - total_current_seconds, 1)
                else:
                    time_spent = 0.0

                # Update active history trackers
                if turn == "White":
                    last_white_clock = total_current_seconds
                else:
                    last_black_clock = total_current_seconds
            except IndexError, ValueError:
                pass

        # 2. Generate the SAN string BEFORE pushing the move to the board
        move_san = board.san(move)

        # 3. Advance the virtual board state
        board.push(move)

        # 4. Analyze position with Stockfish
        info = engine_stockfish.analyse(board, chess.engine.Limit(time=0.1))
        score = info["score"]

        if score.is_mate():
            eval_str = f"M{score.white().mate()}"
        else:
            eval_str = f"{score.white().score() / 100:+.2f}"

        # 5. Build and append the validated Pydantic model
        move_obj = ChessMoveSchema(
            move_num=move_number,
            turn=turn,
            san=move_san,
            fen=board.fen(),
            clock_time=clock_time,
            time_spent=time_spent,
            stockfish_eval=eval_str,
        )
        parsed_moves.append(move_obj)

        if turn == "Black":
            move_number += 1

        # Shift our pointer to the next node to advance the loop
        node = next_node

    engine_stockfish.close()
    return ChessGameSchema(
        game_url=game_url,
        white_player=white,
        black_player=black,
        game_date=date,
        eco_url=eco_url,
        moves=parsed_moves,
    )
