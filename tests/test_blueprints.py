import pytest
from flask import Flask
from flask_mux import Mux
from testing.test_cases.router import auth_router, api_router, admin_router


@pytest.fixture
def mux():
    app = Flask(__name__)
    mux = Mux(app)
    mux.use('/auth', auth_router)
    mux.use('/api', api_router)
    mux.use('/admin', admin_router)
    return mux


def test_registered(mux: Mux):
    assert mux.rules.get('auth')
    assert mux.rules.get('api')
    assert mux.rules.get('admin')


def test_router_rules(mux: Mux):
    assert len(mux.rules.get('auth')) == len(auth_router.routes)
    assert len(mux.rules.get('api')) == len(api_router.routes)
    assert len(mux.rules.get('admin')) == len(admin_router.routes)
