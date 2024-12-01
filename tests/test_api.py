# tests/test_api.py
import pytest
from src.app import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_key_value(client):
    # Test creating a new key-value pair
    response = client.put('/kv/test_key', 
                         data=json.dumps({'value': 'test_value'}),
                         content_type='application/json')
    assert response.status_code == 201
    assert b'created' in response.data

    # Test duplicate key
    response = client.put('/kv/test_key', 
                         data=json.dumps({'value': 'another_value'}),
                         content_type='application/json')
    assert response.status_code == 409

def test_read_key_value(client):
    # Create a key-value pair first
    client.put('/kv/test_key', 
               data=json.dumps({'value': 'test_value'}),
               content_type='application/json')

    # Test reading existing key
    response = client.get('/kv/test_key')
    assert response.status_code == 200
    assert b'test_value' in response.data

    # Test reading non-existent key
    response = client.get('/kv/nonexistent_key')
    assert response.status_code == 404

def test_delete_key_value(client):
    # Create a key-value pair first
    client.put('/kv/test_key', 
               data=json.dumps({'value': 'test_value'}),
               content_type='application/json')

    # Test deleting existing key
    response = client.delete('/kv/test_key')
    assert response.status_code == 200

    # Verify key is deleted
    response = client.get('/kv/test_key')
    assert response.status_code == 404

    # Test deleting non-existent key
    response = client.delete('/kv/nonexistent_key')
    assert response.status_code == 404

def test_invalid_requests(client):
    # Test missing value in create request
    response = client.put('/kv/test_key', 
                         data=json.dumps({}),
                         content_type='application/json')
    assert response.status_code == 400

    # Test invalid JSON
    response = client.put('/kv/test_key', 
                         data='invalid json',
                         content_type='application/json')
    assert response.status_code == 400