import io

import chess.pgn
import requests

import chess_db.parser as p


def main() -> None:
    url = f"https://api.chess.com/pub/player/grvmar/games/2026/09/pgn"
    headers = {"User-Agent": "MyChessAnalysisApp/2.0"}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        pgn_data = io.StringIO(response.text)
        while True:
            game = chess.pgn.read_game(pgn_data)
            if game is None:
                break
            print(p.parse_game(game))
            break
