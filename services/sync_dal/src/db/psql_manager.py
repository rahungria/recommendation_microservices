import psycopg2
from sqlite3 import dbapi2

from src import conf


_conn = None


def get_connection() -> dbapi2.Connection:
    global _conn
    if not _conn:
        print(
            'lazy connecting to:'
            f'{conf.POSTGRES_HOST}://{conf.POSTGRES_DB}@{conf.POSTGRES_USER}'
        )
        _conn = psycopg2.connect(
            host=conf.POSTGRES_HOST,
            database=conf.POSTGRES_DB,
            user=conf.POSTGRES_USER,
            password=conf.POSTGRES_PASSWORD
        )
    return _conn
