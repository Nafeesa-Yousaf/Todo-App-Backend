import os
import psycopg2 
from psycopg2 import pool
from contextlib import contextmanager
from decouple import config

from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or config("DATABASE_URL", default=None)

if not DATABASE_URL:
    raise ValueError("Neither DATABASE_URL nor POSTGRES_URL environment variables were found.")

# Clean up DATABASE_URL by removing unsupported query parameters like "supa"
if DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"):
    parsed = urlparse(DATABASE_URL)
    query_params = parse_qsl(parsed.query)
    # Exclude 'supa' or any other query parameters that psycopg2 doesn't accept
    clean_params = [(k, v) for k, v in query_params if k != "supa"]
    DATABASE_URL = urlunparse(parsed._replace(query=urlencode(clean_params)))

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

