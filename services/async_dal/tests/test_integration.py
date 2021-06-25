import time
import redis
import pytest
import uuid
import sqlite3
import random

from src import conf
from src.db import model_db


conf.initialize()


@pytest.fixture
def _uuid():
    return uuid.uuid4().hex

@pytest.fixture
def client():
    return redis.Redis(conf.REDIS_HOST, conf.REDIS_PORT)


@pytest.mark.integration
def test_search_model_flow(client: redis.Redis, _uuid: str):
    username = uuid.uuid4().hex
    status = "BUILDING"
    msg = {
        'username': username,
        'sender_uuid': _uuid
    }
    id = client.xadd(
        'search_model',
        msg
    )
    start_id = int(id.decode('utf-8').split('-')[0])-1
    res = client.xread(
        {f'search_model_response:{_uuid}': str(start_id)},
        count=1,
        block=2*1000
    )
    print(id)
    print(res)
    assert res != [], '2s timeout'
    assert len(res) == 1, res
    assert len(res[0]) == 2, 'really wrong message'
    res_id, res_msg = res[0][1][0]
    # small inconsistencies (1 or 2 ms error)
    # assert res_id == id
    assert res_msg == {
        b'username': username.encode('utf-8'),
        b'status': b'NOT FOUND'
    }, 'should not find user'


@pytest.mark.integration
def test_save_model_flow(client: redis.Redis, _uuid: str):
    username = 'cavalo'
    status = 'FETCHING'
    msg = {
        'username': username,
        'status': status
    }
    id = client.xadd('save_model', msg)
    time.sleep(2)
    res = client.xpending_range('save_model', conf.GROUPNAME, id, id, 1)
    assert res == [], 'save_model message is pending (2s timeout)'
