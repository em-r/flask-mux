import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_mux import Mux
from testing.test_cases.middlewares import test_mws_router


@pytest.fixture
def client():
    app = Flask(__name__)
    mux = Mux(app)
    mux.use('/', test_mws_router)
    return app.test_client()


def test_basic(client: FlaskClient):
    """test GET method with no middlewares"""
    resp = client.get('/basic')
    assert resp.status_code == 200
    assert resp.json.get('success')


def test_one_mw(client: FlaskClient):
    """test GET method with one middlewares"""
    headers = {'admin': 'Mehdi'}
    resp = client.get('/get-with-auth', headers=headers)
    assert resp.status_code == 200
    assert resp.json.get('success')
    assert resp.json.get('admin') == headers.get('admin')


def test_one_mw_failing(client: FlaskClient):
    """test GET method with one middlewares"""
    resp = client.get('/get-with-auth')
    assert resp.status_code == 403
    assert not resp.json.get('success')


def test_multi_mws(client: FlaskClient):
    """test GET method with multiple middlewares"""
    headers = {
        'Authorization': 'whatever',
        'admin': 'Mehdi'
    }
    resp = client.get('/get-with-multi-mws', headers=headers)
    assert resp.status_code == 200
    assert resp.json.get('success')
    assert resp.json.get('admin') == headers.get('admin')


def test_multi_mws_failing(client: FlaskClient):
    """test GET method with multiple middlewares"""
    resp = client.get('/get-with-auth')
    assert resp.status_code == 403
    assert not resp.json.get('success')


def test_extra_mws(client: FlaskClient):
    """test GET method with many middlewares"""
    headers = {
        'Authorization': 'whatever',
        'admin': 'Mehdi'
    }
    resp = client.get('/get-with-extra-mws', headers=headers)
    assert resp.status_code == 200
    assert resp.json.get('success')
    assert resp.json.get('admin') == headers.get('admin')
