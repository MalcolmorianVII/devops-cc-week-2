import random
import pytest
from flask import Flask
from quote_disp.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'healthy'

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'This is the Quote Display Service' in response.data

def test_quote_endpoint(client):
    response = client.get('/quote')
    assert response.status_code == 200
    assert response.data.decode('utf-8') in app.quotes
