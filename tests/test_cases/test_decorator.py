from flask import request
from flask_mux import Router
from tests.test_cases.common import is_json, is_admin, is_auth

tc_default_router = Router()


@tc_default_router.route('/')
def handle_basic():
    return {'success': True}


@tc_default_router.route('/', http_methods=['POST'])
def handle_basic_post():
    return {'success': True}


@tc_default_router.route('/<int:id>/<string:name>')
def handle_with_params(id, name):
    return {'success': True, 'id': id, 'name': name}


@tc_default_router.route('/post', http_methods=['POST'])
def handle_post():
    return {'success': True}


@tc_default_router.route('/many', http_methods=['POST', 'GET'])
def handle_many():
    return {'success': True, 'method': request.method}


tc_mw_router = Router()


@tc_mw_router.route('/one-mw', http_methods=['POST'])
@is_json
def handle_one_mw():
    if isinstance(request.json, dict) or isinstance(request.json, list):
        body = request.json
    else:
        body = {'body': request.json}
    return {'success': True, 'body': body}, 200


@tc_mw_router.route('/multi-mws', http_methods=['POST'])
@is_auth
@is_admin
@is_json
def handle_multi_mws():
    admin = request.headers.get('admin')
    return {'success': True, 'admin': admin}, 200
