import pytest
import random
from string import ascii_letters
from flask import Flask
from flask.testing import FlaskClient
from flask_mux import Mux
from tests.test_cases.test_decorator import tc_default_router


@pytest.fixture
def client():
    app = Flask(__name__)
    mux = Mux(app)
    mux.use('/', tc_default_router)

    return app.test_client()


def test_get(client: FlaskClient):
    """test GET method with no middlewares"""
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json.get('success') == True


def test_post(client: FlaskClient):
    """test POST method with no middlewares"""
    resp = client.post('/')
    assert resp.status_code == 200
    assert resp.json.get('success')


def test_put(client: FlaskClient):
    """test PUT method on an endpoint that doesn't accept PUT requests"""
    resp = client.put('/')
    assert resp.status_code == 405


def test_with_params(client: FlaskClient):
    """test Router.route with path variables"""
    path_param_id = random.randint(0, 100)
    path_param_name = ''.join(random.choices(ascii_letters, k=5))
    resp = client.get(f'/{path_param_id}/{path_param_name}')
    assert resp.status_code == 200
    assert resp.json.get('success')
    assert resp.json.get('id') == path_param_id
    assert resp.json.get('name') == path_param_name


def test_post(client: FlaskClient):
    """test Router.route on a POST-only endpoint"""
    resp = client.post('/post')
    assert resp.status_code == 200
    assert resp.json.get('success')

    resp = client.get('/post')
    assert resp.status_code == 405

    resp = client.delete('/post')
    assert resp.status_code == 405

    resp = client.put('/post')
    assert resp.status_code == 405


def test_multiple_methods(client: FlaskClient):
    """test Router.route on an endpoint with multiple accepted HTTP methods"""
    resp = client.get('/many')
    assert resp.status_code == 200
    assert resp.json.get('method') == 'GET'

    resp = client.post('/many')
    assert resp.status_code == 200
    assert resp.json.get('method') == 'POST'

    resp = client.put('/many')
    assert resp.status_code == 405

    resp = client.delete('/many')
    assert resp.status_code == 405
