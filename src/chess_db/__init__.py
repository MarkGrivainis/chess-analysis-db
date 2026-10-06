import io

import chess.pgn
import click
import requests

import chess_db.parser as p
from chess_db.queries import add_game, create_table


@click.group()
def cli():
    pass


@cli.command()
def init_db():
    create_table()


@cli.command()
def drop_db():
    pass


@cli.command()
def fetch_games():
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
            game_data = p.parse_game(game)
            add_game(game_data.model_dump())
            break
