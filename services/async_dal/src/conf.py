import os
import uuid
import pathlib

import redis


BASEDIR = None
DEBUG = None
REDIS_HOST = None
REDIS_PORT = None
GROUPNAME = None
UUID = None
redis_client = None
READ_STREAMS = None
INITIALIZED = False
POSTGRES_USER = None
POSTGRES_DB = None
POSTGRES_PASSWORD = None
POSTGRES_HOST = None


def initialize():
    global BASEDIR, DEBUG, REDIS_HOST, REDIS_PORT, GROUPNAME, UUID, redis_client, READ_STREAMS, INITIALIZED, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST
    if INITIALIZED:
        print('config already initialized')
    else:
        print('initializing worker', flush=True)
        BASEDIR = pathlib.Path('.')
        DEBUG = int(os.environ['DEBUG'])

        POSTGRES_DB = os.environ['POSTGRES_DB']
        POSTGRES_USER = os.environ['POSTGRES_USER']
        POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
        POSTGRES_HOST = os.environ['POSTGRES_HOST']

        REDIS_HOST = os.environ['REDIS_HOST']
        REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

        GROUPNAME = "DAL"
        UUID = uuid.uuid4().hex

        redis_client = redis.Redis(REDIS_HOST, REDIS_PORT)
        # lazy connection...
        redis_client.keys() 

        # try to create all consumer groups for all the streams
        # as specified in the main docs
        READ_STREAMS = [
            "save_model",
            "save_recommendation"
        ]

        for stream in READ_STREAMS:
            try:
                redis_client.xgroup_create(stream, GROUPNAME, mkstream=True)
                print(f"created consumer group '{GROUPNAME}' and creating stream '{stream}'", flush=True)
            except redis.ResponseError as e:
                if 'BUSYGROUP' not in str(e):
                    raise e
                print(f"created consumer group '{GROUPNAME}'' for already existing'{stream}'", flush=True)

        print(f"Initialized {GROUPNAME} worker:{UUID}", flush=True)
        INITIALIZED = True
