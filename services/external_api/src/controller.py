from src import conf
from src import util
from src import external_api
import json


def process_main_loop(config: conf.Config):
    streams = config.redis_client.xreadgroup(
        groupname=config.CONSUMER_GROUP,
        consumername=config.UUID,
        streams={s:'>' for s in config.READ_STREAMS},
        count=1,
        block=0,
    )
    print(f'Received message: {streams}')
    entries = util.parse_xreadgroup(streams)
    for stream in entries:
        for msg in entries[stream]:
            process_msg(msg['msg'], msg['id'], stream, config)

def process_msg(msg, id, stream, config: conf.Config):
    print(f"Processing message from stream: {stream}")
    if stream == 'fetch_user_list':
        process_fetch_user_list(msg, config)
    elif stream == 'fetch_anime':
        process_fetch_anime(msg, config)
    else:
        raise Exception(f'Invalid Stream: "{stream}"')
    config.redis_client.xack(stream, config.CONSUMER_GROUP, id)


def process_fetch_user_list(msg, config:conf.Config):
    username = msg['username']
    userlist = external_api.get_user(username)
    config.redis_client.xadd(
        'user_list',
        {
            'list': json.dumps(userlist),
            'username': username,
        }
    )


def process_fetch_anime(msg, config:conf.Config):
    anime_id = msg['anime_id']
    anime = external_api.get_anime(anime_id)
    config.redis_client.xadd(
        'anime',
        {
            'anime': json.dumps(anime),
            'username': msg['username']
        }
    )