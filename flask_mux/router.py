from functools import wraps
from typing import List, Callable
from flask_mux.errors import MissingHandlerError, UncallableMiddlewareError


class Route:
    def __init__(self, endpoint: str, view_func: Callable, http_methods: list = None, unwrapped=None):
        self.endpoint: str = endpoint
        self.view_func = view_func
        self.http_methods = http_methods or ['GET']
        self.unwrapped_view_func = unwrapped or self.view_func

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

    def post(self, endpoint: str, *middlewares):
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

        route = self._create_route('POST', endpoint, middlewares)
        self.routes.append(route)

    def _check_middlewares(self, middlewares: list):
        if not middlewares:
            raise MissingHandlerError('no handler was provided')

        for mw in middlewares:
            if not isinstance(mw, Callable):
                raise UncallableMiddlewareError(
                    'middelwares must be callable functions')

    def _create_route(self, method: str, endpoint: str, middlewares: list):
        """Calls the self._wrap_view_func to wrap the view function
        within the provided middlwares, and then creates a new instance
        of the Route class.

        Args:
            method (str): Request's HTTP method to be handled.
            endpoint (str): Request's endpoint.
            middlewares (list): list of middlewares to wrap the view_func.

        Returns: Route
        """
        # extract the view function from the tail of the list
        view_func = middlewares[-1]

        # if there's only one element in the middlewares list
        # that element is the view function, no wrapping needed
        # returning the Route instance
        if len(middlewares) == 1:
            return Route(endpoint, view_func, http_methods=[method])

        # call the self._wrap_view_func to wrap the view_function within
        # the provied the middlewares
        return Route(
            endpoint,
            self._wrap_view_func(view_func, middlewares[:-1]),
            http_methods=[method],
            unwrapped=view_func
        )

    def _wrap_view_func(self, view_func, middlewares: List):
        """ Returns a wrapper that wraps the view function
        within the the middlewares by ''dequeueing'' each middleware
        from the passed middlewares list.

        Args:
            view_func (callable): view function.
            middlewares (list): list of middlewares to wrap the view_func.

        Returns:
            callable: the new wrapped view function that will be passed to
            the Flask.add_url_rule method.
        """
        def wrapper(*args, **kwargs):

            # perform a deep copy of the middlewares list to not mutate it.
            mws = middlewares.copy()
            mw = mws.pop(0)

            # loop until the copied list is empty
            while mws:
                # call each middleware by passing
                # the next one as argument
                mw = mw(mws.pop(0))

            # if current mw is a tuple (not a callable -> not a view func)
            # return the mw since it's the response that will be supplied
            # to Flask
            if isinstance(mw, tuple):
                return mw

            view_fn = mw(view_func)
            if isinstance(view_fn, Callable):
                return view_fn(*args, **kwargs)
            return mw(view_func)
        return wrapper
