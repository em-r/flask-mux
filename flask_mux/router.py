from functools import wraps
from typing import List, Callable


class Router:
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
    def __init__(self, endpoint: str, view_func: Callable, http_methods: list = None):
        self.endpoint: str = endpoint
        self.view_func = view_func
        self.http_methods = http_methods or ['GET']
