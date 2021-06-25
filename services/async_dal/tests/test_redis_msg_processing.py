import pytest 
from src import util


@pytest.fixture(name='entry')
def serialized_entry():
    return [
        [b'stream1', [
            (b'1619290871036-0', {
                b'type': b'shiran1',
                b'msg': b'{"username": "dongers", "timestamp": 1619301249.861807}'
            })
        ]],
        [b'stream2', [
            (b'1619230841236-0', {
                b'type': b'shiran2',
                b'msg': b'{"username": "raphailias", "timestamp": 1619301245.861807}'
            }),
            (b'1619290871124-0', {
                b'type': b'shiran3',
                b'msg': b'{"username": "yoriii750", "timestamp": 1619301240.861807}'
            })
        ]],
        [b'stream3', [
            (b'1619293871036-0', {
                b'username': b'dongers',
                b'animes': b'[12, 233, 12, 1, 41, 12, 3]'
            })
        ]],
        [b'stream4', [
            (b'2612233475068-0', {
                b"sender_uuid": b"1ad12318f6a9a",
                b"username": b"raphailias",
                b"anime_id": b'102',
                b"status": b"CREATED",
                b"recommendation": b'12'
            })
        ]],
    ]


@pytest.fixture(name='ds_entry')
def deserialized_entry():
    return {
        'stream1': [{
            "id": "1619290871036-0",
            'msg':{
                'type': 'shiran1',
                'msg': {"username": "dongers", "timestamp": 1619301249.861807}
            }
        }],
        'stream2': [
            {
                'id': '1619230841236-0',
                'msg': {
                    'type': 'shiran2',
                    'msg': {"username": "raphailias", "timestamp": 1619301245.861807}
                }
            },
            {
                'id': '1619290871124-0',
                'msg': {
                    'type': 'shiran3',
                    'msg': {"username": "yoriii750", "timestamp": 1619301240.861807}
                }
            }
        ],
        'stream3': [{
            "id": "1619293871036-0",
            'msg':{
                'username': 'dongers',
                'animes': [12, 233, 12, 1, 41, 12, 3]
            }
        }],
        'stream4': [{
            "id": "2612233475068-0",
            'msg':{
                "sender_uuid": "1ad12318f6a9a",
                "username": "raphailias",
                "anime_id": 102,
                "status": "CREATED",
                "recommendation": 12
            }
        }],
    }


def test_deserialize_dict(entry, ds_entry):
    assert util.deserialize_msg(entry[0][1][0][1]) == ds_entry['stream1'][0]['msg']

def test_entry_deserializer(entry, ds_entry):
    assert util.parse_xreadgroup(entry) == ds_entry
