import json


VALID_STATUS = ('CREATED', 'BUILDING', 'FETCHING', 'NOT FOUND')


def deserialize_msg(msg: dict):
    '''
    parses a dict msg from a redis stream
    msg: the message from a redis stream in the format
    dict[bytes, bytes(serialized json)]
    '''
    def decode_value(val):
        try:
            return json.loads(val)
        except json.decoder.JSONDecodeError:
            return val.decode('utf-8')
    return {
        key.decode('utf-8'): decode_value(value)
        for key, value in msg.items()
    }


def parse_xreadgroup(stream_response: list):
    '''
    receives redis read response with awful format
    (list of list of list of bytes) to a dict with 
    beautiful format.
    
    format = { 'stream_name' : [ { 'msg_id' : dict_msg } ] }

    stream_response: redis xreadgroup response
    '''
    return {
        stream_obj[0].decode('utf-8'):
        [
            {
                'id':id.decode('utf-8'),
                'msg': deserialize_msg(msg)
            }
            for id,msg in stream_obj[1]
        ]
        for stream_obj in stream_response 
    }


def msg_count(stream_response: list):
    i = 0
    for stream in stream_response:
        i += len(stream[1])
