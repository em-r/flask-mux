from functools import wraps
from typing import List, Callable, Sequence
from flask_mux.errors import MissingHandlerError, UncallableMiddlewareError


class Route:
    """Object representation of a route.

    As the name implies, the Route class represents a route
    by keeping track of the endpoint in question, the allowed
    HTTP methods to be handled by the route, the view function
    that is wrapped within middlewares which will be envoked
    when a request hits the endpoint and the pure view function.

    The created instance will be used to create the url rule
    which will be registered to the Flask url map.


    Properties:
        endpoint (str):
            the endpoint to be handled.

        http_methods (List[str]):
            list of the HTTP methods that are allowed within the route.

        view_func (Callable):
            the view function wrapped within the provided middlewares
            which will be registred with url rule.

        unwrapped_view_func (Callable):
            the unwrapped version of the view function.

    """

    def __init__(
        self,
        endpoint: str,
        view_func: Callable,
        http_methods: list = None,
        unwrapped=None,
    ):
        self.endpoint: str = endpoint
        self.http_methods = http_methods or ["GET"]
        self.view_func = view_func
        self.unwrapped_view_func = unwrapped or self.view_func

    def __repr__(self):
        return f"{self.endpoint} -> {self.http_methods}"

    @classmethod
    def create(cls, endpoint: str, methods: Sequence[str], middlewares: list):
        """Calls the :meth`_wrap_view_func` to wrap the view function
        within the provided middlwares, and then creates a new instance
        of the Route class.

        Args:
            endpoint (str): Request's endpoint.
            methods (Sequence): Request's HTTP method to be handled.
            middlewares (list): list of middlewares to wrap the
            view_func.

        Returns: Route
        """

        # methods param must be an sequence (e.g: list, tuple)
        # otherwise raise an assertionError
        assert isinstance(methods, Sequence)

        # extract the view function from the tail of the list
        view_func = middlewares[-1]

        # if there's only one element in the middlewares list
        # that element is the view function, no wrapping needed
        # returning the Route instance
        if len(middlewares) == 1:
            return cls(endpoint, view_func, http_methods=[*set(methods)])

        # call the self._wrap_view_func to wrap the view_function within
        # the provied the middlewares
        return cls(
            endpoint,
            cls._wrap_view_func(view_func, middlewares[:-1]),
            http_methods=[*set(methods)],
            unwrapped=view_func,
        )

    @staticmethod
    def _wrap_view_func(view_func, middlewares: List):
        """Returns a wrapper that wraps the view function
        within the the middlewares by `dequeueing` each middleware
        from the passed middlewares list.

        Args:
            view_func (callable): view function.
            middlewares (list): list of middlewares to wrap the
            view_func.

        Returns:
            callable: the new wrapped view function that will be passed
            to the Flask.add_url_rule method.
        """

        def wrapper(*args, **kwargs):

            # perform a deep copy of the middlewares list to not
            # mutate it.
            mws = middlewares.copy()
            mw = mws.pop(0)

            # loop until the copied list is empty
            while mws:
                # call each middleware by passing
                # the next one as argument
                mw = mw(mws.pop(0))

            # if current mw is a tuple
            # (not a callable -> not a view func)
            # return the mw since it's the response that will be
            # supplied to Flask
            if isinstance(mw, tuple):
                return mw

            view_fn = mw(view_func)
            if isinstance(view_fn, Callable):
                return view_fn(*args, **kwargs)
            return mw(view_func)

        return wrapper


class Router:
    """A router that stores routes defined within a namespace.

    The Router class implements a set of methods
    that can be used to create new routes within a certain
    namespace, which should be provided one registering
    the Router with Mux.use method


    A typical example:

        auth_router = Router()
        auth_router.post('/signin', signin_func)
        auth_router.post('/signup', signup_func)

        mux = Mux(app)
        mux.use('/auth', auth_router)


    Properties:
        routes (List[Route]):
            list of the routes defined within the namespace.
            those routes are appended to the list automatically
            when created using the methods the Router class
            implements.
    """

    def __init__(self):
        self.routes: List[Route] = []

    def route(self, endpoint: str, http_methods: list = None):
        """Acts similarly to :meth:`Flask.route` decorator.
        Appends a new Route instance to the self.routes list
        which will be used to register all the routes with their
        endpoints.

        Args:
            endpoint (str): endpoint to handle.
            http_methods (list): allowed HTTP methods for the given
            endpoint.
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
            middlewares (*Callable): variadic param representing
            a sequence of middlewares.
        """
        route = self._create_route(endpoint, ["GET"], *middlewares)
        self.routes.append(route)

    def post(self, endpoint: str, *middlewares):
        """Handles incoming HTTP POST requests
        by executing the passed middlewares in
        their respective order.

        Args:
            endpoint (str): endpoint to handle.
            middlewares (*Callable): variadic param representing
            a sequence  of middlewares.
        """
        route = self._create_route(endpoint, ["POST"], *middlewares)
        self.routes.append(route)

    def put(self, endpoint: str, *middlewares):
        """Handles incoming HTTP PUT requests
        by executing the passed middlewares in
        their respective order.

        Args:
            endpoint (str): endpoint to handle.
            middlewares (*Callable): variadic param representing
            a sequence of middlewares.
        """
        route = self._create_route(endpoint, ["PUT"], *middlewares)
        self.routes.append(route)

    def delete(self, endpoint: str, *middlewares):
        """Handles incoming HTTP DELETE requests.
        Executes the passed middlewares in their respective order.

        Args:
            endpoint (str): endpoint to handle.
            middlewares (*Callable): variadic param representing a
            sequence of middlewares.
        """
        route = self._create_route(endpoint, ["DELETE"], *middlewares)
        self.routes.append(route)

    def patch(self, endpoint: str, *middlewares):
        """Handles incoming HTTP PATCH requests.
        Executes the passed middlewares in their respective order.

        Args:
            endpoint (str): endpoint to handle.
            middlewares (*Callable): variadic param representing a
            sequence of middlewares.
        """
        route = self._create_route(endpoint, ["PATCH"], *middlewares)
        self.routes.append(route)

    def handle(self, endpoint: str, *middlewares):
        """Handles all incoming requests regardless of the HTTP method
        and executes the passed middlewares in their respective order.

        Args:
            endpoint (str): endpoint to handle.
            middlewares (*Callable): variadic param representing
            a sequence of middlewares.
        """
        route = self._create_route(
            endpoint, ["GET", "POST", "PUT", "DELETE", "PATCH"], *middlewares
        )
        self.routes.append(route)

    @staticmethod
    def _check_middlewares(middlewares: list):
        """Checks if the provided middlawares are valid callable
        objects."""

        if not middlewares:
            raise MissingHandlerError("no handler was provided")

        for mw in middlewares:
            if not isinstance(mw, Callable):
                raise UncallableMiddlewareError(
                    "middelwares must be callable functions"
                )

    def _create_route(
        self, endpoint: str, http_methods: Sequence, *middlewares
    ) -> Route:
        """Creates a new Route after checking if the provided
        middlewares are valid by calling :meth:`_check_middlewares`
        on them.

        Args:
            endpoint (str): Request's endpoint.
            methods (Sequence): Request's HTTP method to be handled.
            middlewares (variadic): list of middlewares to wrap the
            view_func.

        Returns: Route
        """
        middlewares = list(middlewares)
        self._check_middlewares(middlewares)

        return Route.create(endpoint, http_methods, middlewares)
