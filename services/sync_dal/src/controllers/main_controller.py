from src import util
from src.db import model_db
from src.db import rec_db
from src.db import psql_manager


def search_model(username: str):
    conn = psql_manager.get_connection()
    model = model_db.search_model(conn, username)
    return model


def search_recommendation(username:str, anime_id:str):
    conn = psql_manager.get_connection()
    rec = rec_db.search_rec(conn, username, anime_id)
    return rec
