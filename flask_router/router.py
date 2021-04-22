from flask import Flask
from flask_router.http_router import HTTPRouter, Route


class Router:

    def __init__(self, app: Flask):
        self.app = app
        self.rules = []

    def use(self, namespace: str, router: HTTPRouter):
        for route in router.routes:
            rule = f'{namespace}/{route.endpoint}'
            endpoint = f'{namespace}.{route.view_func.__name__}'

            self.app.add_url_rule(
                rule, endpoint, route.view_func, methods=route.http_methods)

            rule = Rule(rule, endpoint, route.view_func)
            self.rules.append(rule)


class Rule:
    def __init__(self, rule, endpoint, view_func):
        self.rule = rule
        self.endpoint = endpoint
        self.view_func = view_func
