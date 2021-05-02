import unittest
from flask import Flask
from flask_mux import Mux
from tests.test_mws_cases import test_mws_router


class TestMwsGET(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.mux = Mux(self.app)
        self.mux.use('/', test_mws_router)

        self.client = self.app.test_client()

    def test_basic(self):
        resp = self.client.get('/basic')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))

    def test_one_mw(self):
        headers = {'admin': 'Mehdi'}
        resp = self.client.get('/get-with-auth', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('admin'), headers.get('admin'))

    def test_one_mw_failing(self):
        resp = self.client.get('/get-with-auth')
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(resp.json.get('success'))

    def test_multi_mws(self):
        headers = {
            'Authorization': 'whatever',
            'admin': 'Mehdi'
        }
        resp = self.client.get('/get-with-multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('admin'), headers.get('admin'))

    def test_multi_mws_failing(self):
        resp = self.client.get('/get-with-auth')
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(resp.json.get('success'))

    def test_extra_mws(self):
        headers = {
            'Authorization': 'whatever',
            'admin': 'Mehdi'
        }
        resp = self.client.get('/get-with-extra-mws', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('admin'), headers.get('admin'))


class TestMwsPOST(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.mux = Mux(self.app)
        self.mux.use('/', test_mws_router)

        self.client = self.app.test_client()

    def test_basic(self):
        resp = self.client.post('/basic')
        self.assertEqual(resp.status_code, 200)

    def test_one_mw(self):
        body = {'message': 'samcro'}
        resp = self.client.post('/one-mw', json=body)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_one_mw_failing(self):
        resp = self.client.post('/one-mw')
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.json.get('success'))

    def test_multi_mws(self):
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever'}
        resp = self.client.post('/multi-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_multi_mws_failing(self):
        body = {'message': 'samcro'}
        resp = self.client.post('/multi-mws', json=body)

        self.assertEqual(resp.status_code, 401)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'unauthorized access')

    def test_extra_mws(self):
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever', 'admin': 'Mehdi'}
        resp = self.client.post('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('admin'), headers.get('admin'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_extra_mws_failing_1(self):
        body = {'message': 'samcro'}
        headers = {'admin': 'Mehdi'}
        resp = self.client.post('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 401)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'unauthorized access')

    def test_extra_mws_failing_2(self):
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever'}
        resp = self.client.post('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 403)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'only admins are allowed')

    def test_extra_mws_failing_3(self):
        headers = {'Authorization': 'whatever', 'admin': 'Mehdi'}
        resp = self.client.post('/extra-mws', headers=headers)

        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.json.get('success'))


if __name__ == '__main__':
    unittest.main()
