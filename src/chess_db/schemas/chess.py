from pydantic import BaseModel


class ChessMoveSchema(BaseModel):
    move_num: int
    turn: str
    san: str
    fen: str
    clock_time: str | None = None
    stockfish_eval: str


class ChessGameSchema(BaseModel):
    game_url: str
    white_player: str
    black_player: str
    game_date: str | None = None
    eco_url: str
    moves: list[ChessMoveSchema] = []
