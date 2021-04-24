from functools import wraps
from flask import request
import json


def is_json(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return {'success': False, 'message': 'request body must be valid json'}, 400
        return view_func(*args, **kwargs)
    return wrapper


def is_admin(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):

        if not request.headers.get('admin'):
            return {'success': False, 'message': 'only admins are allowed'}, 403

        return view_func(*args, **kwargs)
    return wrapper
