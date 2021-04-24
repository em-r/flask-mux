import unittest
import random
from string import ascii_letters
from flask import Flask
from flask_mux import Mux
from tests.test_decorator_cases import tc_default_router


class TestBasic(unittest.TestCase):
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

    def test_post(self):
        resp = self.client.post('/post')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))

        resp = self.client.get('/post')
        self.assertEqual(resp.status_code, 405)

        resp = self.client.delete('/post')
        self.assertEqual(resp.status_code, 405)

        resp = self.client.put('/post')
        self.assertEqual(resp.status_code, 405)

    def test_multiple_methods(self):
        resp = self.client.get('/many')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), 'GET')

        resp = self.client.post('/many')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), 'POST')

        resp = self.client.put('/many')
        self.assertEqual(resp.status_code, 405)

        resp = self.client.delete('/many')
        self.assertEqual(resp.status_code, 405)


if __name__ == '__main__':
    unittest.main()
