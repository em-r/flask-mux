from functools import wraps
from typing import List


class HTTPRouter:
    def __init__(self):
        self.routes: List[Route] = []

    def get(self, endpoint: str):
        def decorator(view_func):
            route = Route(endpoint, view_func)
            self.routes.append(route)

            @wraps(view_func)
            def wrapper(*args, **kwargs):

                return view_func(*args, **kwargs)
            return wrapper
        return decorator


class Route:
    def __init__(self, endpoint, view_func, http_methods=None):
        self.endpoint = endpoint
        self.view_func = view_func
        self.http_methods = http_methods or ['GET']
