import requests
import pytest
import threading
from quote_disp.app import app

def start_flask_app():
    app.run(host="0.0.0.0", port=5000, debug=True)

@pytest.fixture(scope="module")
def setup_flask_app():
    # Start the Flask app in a separate thread
    thread = threading.Thread(target=start_flask_app)
    thread.start()

    # Wait for the app to start
    import time
    time.sleep(2)

    yield app

    # Clean up after the tests
    thread.join()

def test_e2e_home(setup_flask_app):
    app = setup_flask_app
    response = requests.get("http://127.0.0.1:5000/")
    assert response.status_code == 200
    assert b'This is the Quote Display Service' in response.content

def test_e2e_health(setup_flask_app):
    app = setup_flask_app
    response = requests.get("http://127.0.0.1:5000/health")
    assert response.status_code == 200
    assert response.content == b'healthy'

def test_e2e_quote(setup_flask_app):
    app = setup_flask_app
    response = requests.get("http://127.0.0.1:5000/quote")
    assert response.status_code == 200
    assert response.content.decode('utf-8') in app.quotes
