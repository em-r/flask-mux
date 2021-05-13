from flask.testing import FlaskClient


def test_basic(client: FlaskClient, method):
    """test POST method with no middlewares"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    resp = req_func('/basic')
    assert resp.status_code == 200


def test_one_mw(client: FlaskClient, method):
    """test POST method with one middleware"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    body = {'message': 'samcro'}
    resp = req_func('/one-mw', json=body)

    assert resp.status_code, 200
    assert resp.json.get('success')
    assert resp.json.get('req_body'), body


def test_one_mw_failing(client: FlaskClient, method):
    """test POST method with one middleware"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    resp = req_func('/one-mw')
    assert resp.status_code == 400
    assert not resp.json.get('success')


def test_multi_mws(client: FlaskClient, method):
    """test POST method with multiple middleware"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    body = {'message': 'samcro'}
    headers = {'Authorization': 'whatever'}
    resp = req_func('/multi-mws', json=body, headers=headers)

    assert resp.status_code == 200
    assert resp.json.get('success')
    assert resp.json.get('req_body') == body


def test_multi_mws_failing(client: FlaskClient, method):
    """test POST method with multiple middleware"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    body = {'message': 'samcro'}
    resp = req_func('/multi-mws', json=body)

    assert resp.status_code == 401
    assert not resp.json.get('success')
    assert resp.json.get('message') == 'unauthorized access'


def test_extra_mws(client: FlaskClient, method):
    """test POST method with many middleware"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    body = {'message': 'samcro'}
    headers = {'Authorization': 'whatever', 'admin': 'Mehdi'}
    resp = req_func('/extra-mws', json=body, headers=headers)

    assert resp.status_code == 200
    assert resp.json.get('success')
    assert resp.json.get('admin') == headers.get('admin')
    assert resp.json.get('req_body') == body


def test_extra_mws_failing_1(client: FlaskClient, method):
    """test POST method with many middleware"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    body = {'message': 'samcro'}
    headers = {'admin': 'Mehdi'}
    resp = req_func('/extra-mws', json=body, headers=headers)

    assert resp.status_code, 401
    assert not resp.json.get('success')
    assert resp.json.get('message'), 'unauthorized access'


def test_extra_mws_failing_2(client: FlaskClient, method):
    """test POST method with many middleware"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    body = {'message': 'samcro'}
    headers = {'Authorization': 'whatever'}
    resp = req_func('/extra-mws', json=body, headers=headers)

    assert resp.status_code == 403
    assert not resp.json.get('success')
    assert resp.json.get('message') == 'only admins are allowed'


def test_extra_mws_failing_3(client: FlaskClient, method):
    """test POST method with many middleware"""
    assert method in ['get', 'post', 'put', 'delete', 'patch']

    req_func = getattr(client, method)
    headers = {'Authorization': 'whatever', 'admin': 'Mehdi'}
    resp = req_func('/extra-mws', headers=headers)

    assert resp.status_code, 400
    assert not resp.json.get('success')
