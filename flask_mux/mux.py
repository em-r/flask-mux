from flask import Flask
from flask_mux.router import Router, Route


class Mux:
    def __init__(self, app: Flask):
        self.app = app
        self.rules = []

    def use(self, namespace: str, router: Router):
        """Registers all the router's routes with their endpoints
        in the provided namespace.

        Example:

            use('/auth', auth_router) will take all the routes created
            using the auth_router, prepend '/auth' to each route's endpoint
            and then register the route with the final endpoint.

        Args:
            namespace (str): namespace which the routes will be mapped to.
            router (Router): router instance with the registered routes.
        """
        for route in router.routes:
            rule = self._create_rule(namespace, route)

            if rule.view_func:
                self.app.add_url_rule(
                    rule.rule, rule.endpoint, rule.view_func, methods=route.http_methods)

                self.rules.append(rule)

    def _create_rule(self, namespace: str, route: Route) -> Rule:
        """Creates a Rule instance with the correct url rule and endpoint.

        Args:
            namespace (str): namespace which the route param will be mapped to.
            route (Route): route instance that will be registered with the provided namespace.
        """

        _namespace = namespace.strip('/')
        _endpoint = route.endpoint.strip('/')

        # if namespace = '/' -> no modifications are needed for url rule and the endpoint
        if _namespace == '':
            return Rule(route.endpoint, route.view_func.__name__, route.view_func)

        """example for namespace != '/':
        namespace='/auth'       Route.endpoint='/login'     view_func.__name__='login_func'
        
        --> Rule.rule = '/auth/login'
        --> Rule.endpoint = 'auth.login_func'
        """

        url_rule = f'/{_namespace}/{_endpoint}'
        endpoint = f'{_namespace}.{route.view_func.__name__}'
        return Rule(url_rule, endpoint, route.view_func)


class Rule:
    def __init__(self, rule: str = '', endpoint: str = '', view_func: callable = None):
        self.rule = rule
        self.endpoint = endpoint
        self.view_func = view_func

    def __repr__(self):
        return f'rule: {self.rule} | endpoint: {self.endpoint}'
