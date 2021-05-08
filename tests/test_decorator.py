import unittest
import random
from string import ascii_letters
from tests.test_base import FlaskMuxBaseTest
from tests.test_cases.test_decorator import tc_default_router, tc_mw_router


class TestBasic(FlaskMuxBaseTest):
    def setUp(self):
        super().setUp()
        self.mux.use('/', tc_default_router)

    def test_default(self):
        """test Router.route on a GET-only method"""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))

        resp = self.client.post('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))

        resp = self.client.put('/')
        self.assertEqual(resp.status_code, 405)

    def test_with_params(self):
        """test Router.route with path variables"""
        path_param_id = random.randint(0, 100)
        path_param_name = ''.join(random.choices(ascii_letters, k=5))
        resp = self.client.get(f'/{path_param_id}/{path_param_name}')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('id'), path_param_id)
        self.assertEqual(resp.json.get('name'), path_param_name)

    def test_post(self):
        """test Router.route on a POST-only endpoint"""
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
        """test Router.route on an endpoint with multiple accepted HTTP methods"""
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


class TestWithMiddlewares(FlaskMuxBaseTest):
    def setUp(self):
        super().setUp()
        self.mux.use('/', tc_mw_router)

    def test_one_mw(self):
        """test Router.route with one middleware"""
        headers = {'content-type': 'application/json'}
        body = {'message': 'bit dodgy mate!'}
        resp = self.client.post('/one-mw', headers=headers, json=body)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('success'), True)
        self.assertEqual(resp.json.get('body'), body)

    def test_one_mw_failing(self):
        """test Router.route with one middleware"""
        resp = self.client.post('/one-mw')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json.get('success'), False)

        headers = {'content-type': 'application/json'}
        resp = self.client.put('/one-mw', headers=headers)
        self.assertEqual(resp.status_code, 405)

    def test_multi_mws(self):
        """test Router.route with multiple middlewares"""
        admin = 'Mehdi'
        headers = {
            'content-type': 'application/json',
            'admin': admin,
            'Authorization': 'whatever'
        }
        resp = self.client.post('/multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('success'), True)
        self.assertEqual(resp.json.get('admin'), admin)

        resp = self.client.post('/multi-mws')
        self.assertEqual(resp.status_code, 401)

        headers = {
            'Authorization': 'whatever',
        }
        resp = self.client.post('/multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 403)

        headers = {
            'admin': admin,
            'Authorization': 'whatever'
        }
        resp = self.client.post('/multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 400)

    def test_multi_mws_failing_1(self):
        """test Router.route with multiple middlewares"""
        headers = {'admin': 'Mehdi'}
        resp = self.client.post('/multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json.get('success'), False)
        self.assertEqual(resp.json.get('message'),
                         'unauthorized access')

    def test_multi_mws_failing_2(self):
        """test Router.route with multiple middlewares"""
        headers = {'content-type': 'application/json'}
        resp = self.client.post('/multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json.get('success'), False)
        self.assertEqual(resp.json.get('message'), 'unauthorized access')

    def test_multi_mws_preserve_order(self):
        """test Router.route with multiple middlewares (order preserving)"""
        resp = self.client.post('/multi-mws')
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json.get('success'), False)
        self.assertEqual(resp.json.get('message'), 'unauthorized access')


if __name__ == '__main__':
    unittest.main()
