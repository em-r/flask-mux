from functools import wraps
from typing import List, Callable
from flask_mux.errors import MissingHandlerError, UncallableMiddlewareError


class Route:
    def __init__(self, endpoint: str, view_func: Callable, http_methods: list = None):
        self.endpoint: str = endpoint
        self.view_func = view_func
        self.http_methods = http_methods or ['GET']

    def __repr__(self):
        return f'{self.endpoint} -> {self.http_methods}'


class Router:
    def __init__(self):
        self.routes: List[Route] = []

    def route(self, endpoint: str, http_methods: list = None):
        """Acts similarly to Flask.route decorator.
        Appends a new Route instance to the self.routes list
        which will be used to register all the routes with their endpoints.

        Args:
            endpoint (str): endpoint to handle.
            http_methods (list): allowed HTTP methods for the given endpoint.
        """
        def decorator(view_func):
            route = Route(endpoint, view_func, http_methods=http_methods)
            self.routes.append(route)

            @wraps(view_func)
            def wrapper(*args, **kwargs):

                return view_func(*args, **kwargs)
            return wrapper
        return decorator

    def get(self, endpoint: str, *middlewares):
        """Handles incoming HTTP GET requests 
        by executing the passed middlewares in
        their respective order.

        Args:
            endpoint (str): endpoint to handle.
            middlewares (*Callable): variadic param representing a sequence 
            of middlewares.
        """
        middlewares = list(middlewares)
        self._check_middlewares(middlewares)

        route = self._create_route('GET', endpoint, middlewares)
        self.routes.append(route)

    def _check_middlewares(self, middlewares):
        if not middlewares:
            raise MissingHandlerError('no handler was provided')

        for mw in middlewares:
            if not isinstance(mw, Callable):
                raise UncallableMiddlewareError(
                    'middelwares must be callable functions')

    def _create_route(self, method: str, endpoint: str, middlewares):
        view_func = middlewares.pop()
        if not middlewares:
            return Route(endpoint, view_func, http_methods=[method])

        mw = middlewares.pop(0)

        while middlewares:
            mw = mw(middlewares.pop(0))

        view_func = mw(view_func)
        return Route(endpoint, view_func, http_methods=[method])
