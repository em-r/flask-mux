import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.wrappers import Response
from flask_mux import Mux
from tests.test_cases.test_mws import test_mws_router


def assert_all(resp: Response, method, code=200):
    assert resp.status_code == code
    assert resp.json.get('method') == method


@pytest.fixture
def client():
    app = Flask(__name__)
    mux = Mux(app)
    mux.use('/', test_mws_router)
    return app.test_client()


def test_get(client: FlaskClient):
    resp = client.get('/handle-basic')
    return assert_all(resp, 'GET')


def test_post(client: FlaskClient):
    resp = client.post('/handle-basic')
    return assert_all(resp, 'POST')


def test_put(client: FlaskClient):
    resp = client.put('/handle-basic')
    return assert_all(resp, 'PUT')


def test_delete(client: FlaskClient):
    resp = client.delete('/handle-basic')
    return assert_all(resp, 'DELETE')
