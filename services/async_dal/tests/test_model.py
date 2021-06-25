from datetime import datetime
import pytest
import sqlite3
import random

from src.db import model_db

@pytest.fixture
def model():
    return random.choice([
        {
            'username': 'carlos',
            'created_at': str(datetime.now().timestamp()),
            'status': 'CREATED'
        },
        {
            'username': 'peixe',
            'created_at': str(datetime.now().timestamp()),
            'status': 'FETCHING'
        },
        {
            'username': 'peepeepoopoo',
            'created_at': str(datetime.now().timestamp()),
            'status': 'NOT FOUND'
        },
    ])

@pytest.fixture
def db():
    connection = sqlite3.connect(':memory:')
    connection.execute(
        '''
        CREATE TABLE model(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT_NULL
        );
        '''
    )
    connection.commit()
    yield connection
    connection.close()

@pytest.fixture
def db_populated(db, model):
    model_db.create_model(db, model['username'], model['status'])
    return db, model


def test_create_invalid_status(db):
    with pytest.raises(AssertionError):
        model_db.create_model(db, 'random', 'INVALID')


def test_create_new_model(db, model):
    assert model_db.search_model(db, model['username']) is None
    model_db.create_model(db, model['username'], model['status'])
    record = model_db.search_model(db, model['username'])
    assert record['username'] == model['username']
    assert record['status'] == model['status']


def test_save_exisiting_model(db_populated):
    db, model = db_populated
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM model;')
    assert cursor.fetchone()[0] == 1

    model_db.create_model(db, model['username'], 'BUILDING')
    cursor.execute('SELECT COUNT(*) FROM model;')
    assert cursor.fetchone()[0] == 2
    new_model = model_db.search_model(db, model['username'])
    assert new_model['status'] == 'BUILDING'
