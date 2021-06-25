import sqlite3


_connection = None


def get_connection(file='db/data.db'):
    global _connection
    if not _connection:
        _connection = sqlite3.connect(file)
        cur = _connection.cursor()
        initialize(cur)
        _connection.commit()

    return _connection


def initialize(cursor):
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL
        );
        '''
    )