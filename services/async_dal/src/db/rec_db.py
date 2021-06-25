import time
from sqlite3.dbapi2 import Connection

from src import util


def create_recommendation(conn: Connection, username: str, anime_id: str, value: float):
    '''
    creates a new model instance
    conn: db connection
    username: model's user
    status: string representing model status
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO recommendation(username, anime_id, timestamp, value)
            VALUES (%s,%s,%s,%s);
            ''',
            (username, anime_id, int(time.time()), value)
        )
    except Exception as e:
        print('failed create recommendation')
        raise e
    finally:
        cursor.close()
