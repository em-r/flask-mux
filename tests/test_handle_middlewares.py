import pytest
from random import choice
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


def test_one_mw(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    headers = {'Authorization': 'whatever'}
    resp = req_func('/handle-one-mw', headers=headers)

    assert resp.status_code == 200
    assert resp.json.get('method') == method


def test_one_mw_failing(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    resp = req_func('/handle-one-mw')

    assert resp.status_code == 401


def test_multi_mws(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    headers = {'Authorization': 'whatever'}
    body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
    resp = req_func('/handle-multi-mws', headers=headers, json=body)

    assert resp.status_code == 200
    assert resp.json.get('method') == method
    assert resp.json.get('req_body') == body


def test_multi_mws_failing_1(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    headers = {'Authorization': 'whatever'}
    resp = req_func('/handle-multi-mws', headers=headers)

    assert resp.status_code == 400


def test_multi_mws_failing_2(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
    resp = req_func('/handle-multi-mws', json=body)

    assert resp.status_code == 401


def test_extra_mws(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    admin = 'mehdi'
    headers = {'Authorization': 'whatever', 'admin': admin}
    body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
    resp = req_func('/handle-extra-mws', headers=headers, json=body)

    assert resp.status_code == 200
    assert resp.json.get('method') == method
    assert resp.json.get('admin') == admin
    assert resp.json.get('req_body') == body


def test_extra_mws_failing_1(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    headers = {'Authorization': 'whatever', 'admin': 'mehdi'}
    resp = req_func('/handle-extra-mws', headers=headers)

    assert resp.status_code == 400


def test_extra_mws_failing_2(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    headers = {'Authorization': 'whatever'}
    body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
    resp = req_func('/handle-extra-mws', headers=headers, json=body)

    assert resp.status_code == 403


def test_extra_mws_failing_3(client: FlaskClient):
    """"""
    # select HTTP method randomly
    methods = ['POST', 'PUT', 'DELETE']
    method = choice(methods)

    req_func = getattr(client, method.lower())
    headers = {'admin': 'mehdi'}
    body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
    resp = req_func('/handle-extra-mws', headers=headers, json=body)

    assert resp.status_code == 401
