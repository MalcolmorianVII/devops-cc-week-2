import pytest
import threading
from flask import Flask
from quote_disp.app import app

# Mocking the external service for testing
external_service_response = "Mocked quote from external service"


def start_flask_app():
    app.run(host="0.0.0.0", debug=True, port=5001)


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
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b'This is the Quote Display Service' in response.data


def test_e2e_get_quote(setup_flask_app, requests_mock):
    app = setup_flask_app

    # Mock the external service response
    external_service_url = "http://web1:5000/quote"
    requests_mock.get(external_service_url, text=external_service_response)

    # Perform the request to the Flask app
    response = app.test_client().get("/get_quote")

    assert response.status_code == 200
    assert f'Mocked quote from external service' in response.data.decode("utf-8")
