from sqlite3 import dbapi2


def search_model(conn: dbapi2.Connection, username: str):
    with conn.cursor() as cursor:
        cursor.execute(
            '''
            SELECT id, username, timestamp, status
            FROM model
            WHERE username = %s
            ORDER BY timestamp DESC;
            ''',
            (username,)
        )
        model = cursor.fetchone()
        if model:
            return {
                'id': model[0],
                'username': model[1],
                'timestamp': model[2],
                'status': model[3]
            }
