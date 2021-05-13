from flask.testing import FlaskClient
import pytest
from flask import Flask
from flask_mux import Mux
from testing.test_cases.middlewares import test_mws_router
from testing import test_router


@pytest.fixture
def client():
    app = Flask(__name__)
    mux = Mux(app)
    mux.use('/', test_mws_router)
    return app.test_client()


def test_basic(client: FlaskClient):
    return test_router.test_basic(client, 'post')


def test_one_mw(client: FlaskClient):
    return test_router.test_one_mw(client, 'post')


def test_one_mw_failing(client: FlaskClient):
    return test_router.test_one_mw_failing(client, 'post')


def test_multi_mws(client: FlaskClient):
    return test_router.test_multi_mws(client, 'post')


def test_multi_mws_failing(client: FlaskClient):
    return test_router.test_multi_mws_failing(client, 'post')


def test_extra_mws(client: FlaskClient):
    return test_router.test_extra_mws(client, 'post')


def test_extra_mws_failing_1(client: FlaskClient):
    return test_router.test_extra_mws_failing_1(client, 'post')


def test_extra_mws_failing_2(client: FlaskClient):
    return test_router.test_extra_mws_failing_2(client, 'post')


def test_extra_mws_failing_3(client: FlaskClient):
    return test_router.test_extra_mws_failing_3(client, 'post')
