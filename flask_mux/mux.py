from flask import Flask
from flask_mux.router import Router, Route


class Rule:
    """Object representation of a URL rule.

    The Rule class is used to represent url rules upon
    when they are being registered using the :meth:`Flask.add_url_rule`
    when calling the :meth:`Mux.use` method on a router.


    Properties:
        rule (str): 
            url rule to be registered.

        endpoint (str): 
            endpoint for the registered rule.

        view_func (callable): 
            function to be called when a request
            hits the endpoint.


    Methods:
        create_from_route(namespace, route):
            Creates a new Rule instance based on the provided
            namespace and Route.
    """

    def __init__(self, rule: str = "", endpoint: str = "", view_func: callable = None):
        self.rule = rule
        self.endpoint = endpoint
        self.view_func = view_func

    def __repr__(self):
        return f"rule: {self.rule} | endpoint: {self.endpoint}"

    @classmethod
    def create_from_route(cls, namespace: str, route: Route):
        """Creates a Rule instance using the provided route properties.

        Args:

            namespace (str): 
                namespace which the route parameter
                will be mapped to.

            route (Route): 
                route instance that will be registered
                with the provided namespace.


        Returns:
            Rule: new Rule instance linked to the provided namespace.
        """

        _namespace = namespace.strip("/")
        _endpoint = route.endpoint.strip("/")

        # if namespace = '/' -> no modifications are needed for url rule and the endpoint
        if _namespace == "":
            return Rule(
                route.endpoint, route.unwrapped_view_func.__name__, route.view_func
            )

        """example for namespace != '/':
            namespace='/auth'      
            Route.endpoint='/login'     
            view_func.__name__='login_func'
        
        --> Rule.rule = '/auth/login'
        --> Rule.endpoint = 'auth.login_func'
        """

        url_rule = f"/{_namespace}/{_endpoint}"
        _namespace = _namespace.replace("/", ".")
        endpoint_path = f"{_namespace}.{route.unwrapped_view_func.__name__}"
        return Rule(url_rule, endpoint_path, route.view_func)


class Mux:
    """An object used as central registry to keep track and
    register :class:`Router` instances.


    Properties:
        app (Flask): instance of the Flask app
        rules (list): list of registered url rules


    Methods:
        use(namespace, route):
            registers routes created within a :class:`Router` instance
            with their endpoints.

    """

    def __init__(self, app: Flask):
        self.app = app
        self.rules = []

    def use(self, namespace: str, router: Router):
        """Registers all the router's routes with their endpoints
        in the provided namespace.


        Example:

            use('/auth', auth_router) will take all the routes created
            using the auth_router, prepend '/auth' to each route's
            endpoint and then register the route with the final
            endpoint.


        Args:
            namespace (str): namespace which the routes will be mapped
            to.
            router (Router): router instance with the registered
            routes.
        """
        for route in router.routes:
            # rule = self._create_rule(namespace, route)
            rule = Rule.create_from_route(namespace, route)

            if rule.view_func:
                self.app.add_url_rule(
                    rule.rule, rule.endpoint, rule.view_func, methods=route.http_methods
                )

                self.rules.append(rule)
