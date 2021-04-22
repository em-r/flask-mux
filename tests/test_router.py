import unittest
import random
from flask import Flask
from flask_router import Router, HTTPRouter
from tests.testcases import tc_1_router


class TestRouterGet(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        router = Router(self.app)
        router.use('/', tc_1_router)

        self.client = self.app.test_client()

    def test_default(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))

    def test_with_params(self):
        path_param = random.randint(0, 100)
        resp = self.client.get(f'/{path_param}')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('id'), path_param)

    def test_not_allowed(self):
        resp = self.client.post(f'/')
        self.assertEqual(resp.status_code, 405)


if __name__ == '__main__':
    unittest.main()
