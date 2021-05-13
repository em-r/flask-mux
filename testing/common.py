from functools import wraps
from flask import request, has_request_context


def is_json(next_middleware):
    """Middleware to check if the request's content-type header is
    set to application/json"""
    @wraps(next_middleware)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return {'success': False, 'message': 'request body must be valid json'}, 400
        return next_middleware(*args, **kwargs)
    return wrapper


def is_admin(next_middleware):
    """Middleware to simulate a user access level check"""
    @wraps(next_middleware)
    def wrapper(*args, **kwargs):

        if not request.headers.get('admin'):
            return {'success': False, 'message': 'only admins are allowed'}, 403

        return next_middleware(*args, **kwargs)
    return wrapper


def is_auth(next_middleware):
    """Middleware to simulate an authentication check"""
    @wraps(next_middleware)
    def wrapper(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return {'success': False, 'message': 'unauthorized access'}, 401
        return next_middleware(*args, **kwargs)
    return wrapper


def mock_middleware(next_middleware):
    @wraps(next_middleware)
    def wrapper(*args, **kwargs):
        assert has_request_context()
        return next_middleware(*args, **kwargs)
    return wrapper
