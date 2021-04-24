import unittest
import random
from string import ascii_letters
from flask import Flask
from flask_mux import Mux
from tests.test_decorator_cases import tc_default_router


class TestDefault(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        router = Mux(self.app)
        router.use('/', tc_default_router)

        self.client = self.app.test_client()

    def test_default(self):
        """test Router.route decorator with GET method"""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))

    def test_with_params(self):
        """test Router.route decorator with path variables"""
        path_param_id = random.randint(0, 100)
        path_param_name = ''.join(random.choices(ascii_letters, k=5))
        resp = self.client.get(f'/{path_param_id}/{path_param_name}')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('id'), path_param_id)
        self.assertEqual(resp.json.get('name'), path_param_name)


if __name__ == '__main__':
    unittest.main()
