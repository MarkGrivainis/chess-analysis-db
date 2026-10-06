import os
from contextlib import contextmanager

import psycopg

DB_URI = os.getenv("DATABASE_URL")


@contextmanager
def get_standalone_connection():
    """Opens a connection, yields it, commits/rolls back, and closes it."""
    if DB_URI is None:
        raise ValueError("DATABASE_URL is not defined as an environment variable.")
    with psycopg.connect(DB_URI) as conn:
        yield conn
