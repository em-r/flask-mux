import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_mux import Mux
from testing.test_cases.decorator import tc_mw_router


@pytest.fixture
def client():
    app = Flask(__name__)
    mux = Mux(app)
    mux.use('/', tc_mw_router)

    return app.test_client()


def test_one_mw(client: FlaskClient):
    """test Router.route with one middleware"""
    headers = {'content-type': 'application/json'}
    body = {'message': 'bit dodgy mate!'}
    resp = client.post('/one-mw', headers=headers, json=body)

    assert resp.status_code == 200
    assert resp.json.get('success')
    assert resp.json.get('body') == body


def test_one_mw_failing(client: FlaskClient):
    """test Router.route with one middleware"""
    resp = client.post('/one-mw')
    assert resp.status_code == 400
    assert not resp.json.get('success')

    headers = {'content-type': 'application/json'}
    resp = client.put('/one-mw', headers=headers)
    assert resp.status_code == 405


def test_multi_mws(client: FlaskClient):
    """test Router.route with multiple middlewares"""
    admin = 'Mehdi'
    headers = {
        'content-type': 'application/json',
        'admin': admin,
        'Authorization': 'whatever'
    }
    resp = client.post('/multi-mws', headers=headers)
    assert resp.status_code == 200
    assert resp.json.get('success')
    assert resp.json.get('admin') == admin

    resp = client.post('/multi-mws')
    assert resp.status_code == 401

    headers = {
        'Authorization': 'whatever',
    }
    resp = client.post('/multi-mws', headers=headers)
    assert resp.status_code == 403

    headers = {
        'admin': admin,
        'Authorization': 'whatever'
    }
    resp = client.post('/multi-mws', headers=headers)
    assert resp.status_code == 400


def test_multi_mws_failing_1(client: FlaskClient):
    """test Router.route with multiple middlewares"""
    headers = {'admin': 'Mehdi'}
    resp = client.post('/multi-mws', headers=headers)
    assert resp.status_code == 401
    assert not resp.json.get('success')
    assert resp.json.get('message') == 'unauthorized access'


def test_multi_mws_failing_2(client: FlaskClient):
    """test Router.route with multiple middlewares"""
    headers = {'content-type': 'application/json'}
    resp = client.post('/multi-mws', headers=headers)
    assert resp.status_code == 401
    assert not resp.json.get('success')
    assert resp.json.get('message'), 'unauthorized access'


def test_multi_mws_preserve_order(client: FlaskClient):
    """test Router.route with multiple middlewares (order preserving)"""
    resp = client.post('/multi-mws')
    assert resp.status_code == 401
    assert not resp.json.get('success')
    assert resp.json.get('message') == 'unauthorized access'
