import time
from sqlite3.dbapi2 import Connection

from src import util


def create_model(conn: Connection, username: str, status: str):
    '''
    creates a new model instance
    conn: db connection
    username: model's user
    status: string representing model status
    '''
    # assert status in util.VALID_STATUS
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO model(username, timestamp, status)
            VALUES (%s,%s,%s);
            ''',
            (username, int(time.time()), status)
        )
    except Exception as e:
        print('failed create model')
        raise e
    finally:
        cursor.close()
