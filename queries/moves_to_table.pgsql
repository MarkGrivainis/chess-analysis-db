-- Convert moves from a jsonb array to a table for a specific game
DROP TYPE IF EXISTS chess_move;

CREATE TYPE chess_move AS (
    fen TEXT,
    san TEXT,
    turn TEXT,
    move_num SMALLINT,
    clock_time TIME,
    time_spent FLOAT,
    stockfish_eval TEXT
);

select
    *
from
    jsonb_populate_recordset(
        null::chess_move,
        (
            SELECT
                moves
            FROM
                chess_games
            WHERE
                id = 1
        )
    )