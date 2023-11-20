import pytest
import responses
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

@responses.activate
def test_quote_endpoint(client):
    service_name = "web1"
    replica_index = 0  # You can iterate over the number of replicas

    hostname = f"{service_name}_{replica_index + 1}"
    url = f"http://{hostname}:5000/quote"
    
    responses.add(responses.GET, url, body="This is a mock quote", status=200)

    response = client.get('/get_quote')

    assert response.status_code == 200
    assert b'This is a mock quote' in response.data
