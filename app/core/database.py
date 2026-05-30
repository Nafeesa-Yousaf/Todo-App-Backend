import psycopg2 
from psycopg2 import pool
from contextlib import contextmanager

DATABASE_URL="postgresql://user:password@localhost:5432/postgres"
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
