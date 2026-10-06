from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

DB_URI = "postgresql://user:password@localhost:5432/dbname"


@contextmanager
def get_standalone_connection():
    """Opens a connection, yields it, commits/rolls back, and closes it."""
    with psycopg.connect(DB_URI, row_factory=dict_row) as conn:
        yield conn
