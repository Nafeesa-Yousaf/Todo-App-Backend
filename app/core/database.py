import os
import psycopg2 
from psycopg2 import pool
from contextlib import contextmanager
from decouple import config

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or config("DATABASE_URL", default=None)

if not DATABASE_URL:
    raise ValueError("Neither DATABASE_URL nor POSTGRES_URL environment variables were found.")

connection_pool=pool.SimpleConnectionPool(
    1,5,DATABASE_URL
)

@contextmanager
def get_db():
    conn=connection_pool.getconn()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        connection_pool.putconn(conn)

