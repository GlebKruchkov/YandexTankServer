import pytest
from main import app


@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True,
    })
    return app.test_client()


def test_put_invalid_key(client):
    response = client.put(data={'no_such_key': 'key', 'value': 'value'})
    assert response.status_code == 400
    assert response.data == b'please provide valid arguments -- key and value\n'


def test_put_invalid_value(client):
    response = client.put(data={'key': 'key', 'no_such_value': 'value'})
    assert response.status_code == 400
    assert response.data == b'please provide valid arguments -- key and value\n'


def test_without_value(client):
    response = client.put(data={'key': 'key'})
    assert response.status_code == 400
    assert response.data == b'please provide valid arguments -- key and value\n'


def test_without_key(client):
    response = client.put(data={'value': 'value'})
    assert response.status_code == 400
    assert response.data == b'please provide valid arguments -- key and value\n'


def test_get_non_existing_key(client):
    response = client.get(headers={'key': 'no_such_key'})
    assert response.status_code == 400
    assert response.data == b'there is no such key-value\n'


def test_empty_get(client):
    resp = client.get('/')
    assert resp.status_code == 400
    assert resp.data == b'please provide valid argument -- key\n'


def test_put_data(client):
    response = client.put(data={'key': 'key', 'value': 'value'})
    assert response.status_code == 200
    assert response.data == b'done'


def test_get_data(client):
    response = client.get(headers={'key': 'key'})
    assert response.status_code == 200
    assert response.data == b'value'
