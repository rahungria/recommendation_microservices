import psycopg2
from src import conf
from sqlite3 import dbapi2


_connection = None

def get_connection() -> dbapi2.Connection:
    global _connection
    if not _connection:
        print(f"""\
            connecting to postgresql://{conf.POSTGRES_HOST}/{conf.POSTGRES_DB}@{conf.POSTGRES_USER}\
        """)
        _connection = psycopg2.connect(
            host=conf.POSTGRES_HOST,
            database=conf.POSTGRES_DB,
            user=conf.POSTGRES_USER,
            password=conf.POSTGRES_PASSWORD
        )
    return _connection
