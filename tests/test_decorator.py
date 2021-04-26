import unittest
import random
from string import ascii_letters
from flask import Flask
from flask_mux import Mux
from tests.test_decorator_cases import tc_default_router, tc_mw_router


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

        resp = self.client.post('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))

        resp = self.client.put('/')
        self.assertEqual(resp.status_code, 405)

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


class TestWithMiddlewares(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        router = Mux(self.app)
        router.use('/', tc_mw_router)

        self.client = self.app.test_client()

    def test_one_mw(self):
        headers = {'content-type': 'application/json'}
        body = {'message': 'bit dodgy mate!'}
        resp = self.client.post('/one-mw', headers=headers, json=body)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('success'), True)
        self.assertEqual(resp.json.get('body'), body)

    def test_one_mw_failing(self):
        resp = self.client.post('/one-mw')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json.get('success'), False)

        headers = {'content-type': 'application/json'}
        resp = self.client.put('/one-mw', headers=headers)
        self.assertEqual(resp.status_code, 405)

    def test_multi_mws(self):
        admin = 'Jax'
        headers = {'content-type': 'application/json', 'admin': admin}
        resp = self.client.post('/multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('success'), True)
        self.assertEqual(resp.json.get('admin'), admin)

    def test_multi_mws_failing_1(self):
        admin = 'Jax'
        headers = {'admin': admin}
        resp = self.client.post('/multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json.get('success'), False)
        self.assertEqual(resp.json.get('message'),
                         'request body must be valid json')

    def test_multi_mws_failing_2(self):
        headers = {'content-type': 'application/json'}
        resp = self.client.post('/multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json.get('success'), False)
        self.assertEqual(resp.json.get('message'), 'only admins are allowed')

    def test_multi_mws_preserve_order(self):
        resp = self.client.post('/multi-mws')
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json.get('success'), False)
        self.assertEqual(resp.json.get('message'), 'only admins are allowed')


if __name__ == '__main__':
    unittest.main()
