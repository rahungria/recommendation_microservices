from sqlite3 import dbapi2


def search_rec(conn:dbapi2.Connection, username:str, anime_id:str):
    with conn.cursor() as cursor:
        cursor.execute(
            '''
            SELECT id, username, anime_id, timestamp, value
            FROM recommendation
            WHERE username = %s AND anime_id = %s
            ORDER BY timestamp DESC;
            ''',
            (username, anime_id)
        )
        rec = cursor.fetchone()
        if rec:
            return {
                'id': rec[0],
                'username': rec[1],
                'anime_id': rec[2],
                'timestamp': rec[3],
                'prediction': rec[4]
            }
