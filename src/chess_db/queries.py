import click
from psycopg.types.json import Jsonb

from chess_db.config.db import get_standalone_connection


def create_table():
    with get_standalone_connection() as conn, conn.cursor() as cur:
        query = """
        DROP TABLE IF EXISTS chess_games;

        CREATE TABLE chess_games (
            id SERIAL PRIMARY KEY,
            game_url TEXT,
            white_player TEXT NOT NULL,
            black_player TEXT NOT NULL,
            game_date TIMESTAMP,
            eco_url TEXT,
            moves JSONB NOT NULL
        );
        """
        cur.execute(query)
        click.echo("chess_games added")


def drop_table():
    with get_standalone_connection() as conn, conn.cursor() as cur:
        query = """
        DROP TABLE IF EXISTS chess_games;
        """
        cur.execute(query)
        click.echo("chess_games dropped")


def add_game(game_data):
    with get_standalone_connection() as conn, conn.cursor() as cur:
        game_data["moves"] = Jsonb(game_data["moves"])
        query = """
        INSERT INTO chess_games (game_url, white_player, black_player, game_date, eco_url, moves)
        VALUES (%(game_url)s, %(white_player)s, %(black_player)s, %(game_date)s, %(eco_url)s, %(moves)s::jsonb)
        RETURNING id;
        """
        cur.execute(query, game_data)
