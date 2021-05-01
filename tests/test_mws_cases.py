from flask import request
from flask_mux import Router
from tests.common import is_auth, is_admin, mock_middleware


def get_basic():
    return {'success': True}


def get_with_auth():
    return {'success': True, 'admin': request.headers.get('admin')}


def get_with_multi_mws():
    return {'success': True, 'admin': request.headers.get('admin')}


def get_with_extra_mws():
    return {'success': True, 'admin': request.headers.get('admin')}


test_mws_router = Router()
test_mws_router.get('/basic', get_basic)
test_mws_router.get('/get-with-auth', is_admin, get_with_auth)
test_mws_router.get('/get-with-multi-mws', is_auth,
                    is_admin, get_with_multi_mws)
test_mws_router.get('/get-with-extra-mws',
                    mock_middleware,
                    mock_middleware,
                    mock_middleware,
                    is_auth,
                    is_admin,
                    get_with_extra_mws
                    )
