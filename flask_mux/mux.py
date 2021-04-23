from flask import Flask
from flask_mux.router import Router, Route


class Mux:
    def __init__(self, app: Flask):
        self.app = app
        self.rules = []

    def use(self, namespace: str, router: Router):
        for route in router.routes:
            rule = self.create_rule(namespace, route)

            if rule.view_func:
                self.app.add_url_rule(
                    rule.rule, rule.endpoint, rule.view_func, methods=route.http_methods)

                self.rules.append(rule)

    def create_rule(self, namespace: str, route: Route):
        endpoint = f'{namespace}.{route.view_func.__name__}'
        rule = Rule(endpoint=endpoint, view_func=route.view_func)
        if route.endpoint == '/':
            rule.rule = namespace
        else:
            endpoint = route.endpoint.lstrip('/')
            rule.rule = f'{namespace}/{route.endpoint}'
        return rule


class Rule:
    def __init__(self, rule: str = '', endpoint: str = '', view_func: callable = None):
        self.rule = rule
        self.endpoint = endpoint
        self.view_func = view_func
