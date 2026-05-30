import psycopg2 
from psycopg2 import pool
from contextlib import contextmanager
from decouple import config

DATABASE_URL=config("DATABASE_URL")
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
