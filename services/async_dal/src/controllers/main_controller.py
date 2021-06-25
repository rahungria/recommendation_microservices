from src import conf
from src import util
# from src.db import sqlite_manager
from src.db import psql_manager
from src.db import model_db
from src.db import rec_db


def process_event_loop():
    streams = conf.redis_client.xreadgroup(
        groupname=conf.GROUPNAME,
        consumername=conf.UUID,
        streams={stream: ">" for stream in conf.READ_STREAMS},
        count=1,
        block=0
    )
    print(f"received message: {streams}")
    entries = util.parse_xreadgroup(streams)
    for stream in entries:
        for obj in entries[stream]:
            process_msg(
                stream=stream,
                id=obj['id'],
                msg=obj['msg']
            )


def process_msg(stream, id, msg):
    '''
    routes the messages to the right flow by stream
    stream: identifier of redis stream
    id: message id
    msg: serialized body of the message (unique format by stream)
    '''
    print(f"processing '{stream}':{id}", flush=True)
    # search for the model
    if stream == "save_model":
        save_model_controller(id, msg)
    elif stream == 'save_recommendation':
        save_recommendation_controller(id, msg)
    else:
        raise Exception(f'Unexpected stream received: {stream}')
    print(f"processed '{stream}:{id}' sucessfully")
    conf.redis_client.xack(stream, conf.GROUPNAME, id)
    
def save_model_controller(id, msg):
    # conn = sqlite_manager.get_connection()
    conn = psql_manager.get_connection()
    try:
        model_db.create_model(conn, msg['username'], msg['status'])
    except KeyError:
        print('bad stream request. ACKing message')
        conn.rollback()
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()


def save_recommendation_controller(id, msg):
    username = msg['username']
    anime_id = msg['anime_id']
    prediction = float(msg['prediction'])

    conn = psql_manager.get_connection()
    try:
        print(f"saving recommendation for: {username}/anime#{anime_id}->{prediction}")
        rec_db.create_recommendation(conn, username, anime_id, prediction)
    except Exception:
        conn.rollback()
    else:
        conn.commit()
        conf.redis_client.set(f'recommendation:{username}:{anime_id}', prediction)
        print('saved successfully')
