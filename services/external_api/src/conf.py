import os
import redis
import uuid


class Config:
    _instance: 'Config' = None

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        try:
            print('initializing config...')
            # ENVIRONMENT VARIABLES
            self.DEBUG = int(os.environ.get('DEBUG', 0))
            self.REDIS_HOST = os.environ['REDIS_HOST']
            self.REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
            self.CONSUMER_GROUP = os.environ.get('CONSUMER_GROUP', 'EXTERNAL_API')
            self.READ_STREAMS = (os.environ.get('READ_STREAMS', 'fetch_user_list fetch_anime')).split(' ')
            self.UUID = uuid.uuid4().hex

            # REDIS CONFIG
            self.redis_client = redis.Redis(
                self.REDIS_HOST, 
                self.REDIS_PORT, 
                decode_responses=True
            )
            # guarantee lazy connection
            self.redis_client.keys()

            # creates the consumer groups for each read stream
            for read_stream in self.READ_STREAMS:
                try:
                    self.redis_client.xgroup_create(read_stream, self.CONSUMER_GROUP, mkstream=True)
                except redis.exceptions.ResponseError as exc:
                    if 'BUSYGROUP' not in str(exc):
                        raise exc

        except Exception as exc:
            print('FAILED INITIALIZING CONFIG...')
            raise exc

        print('config done.')
