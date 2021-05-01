import unittest
from flask import Flask
from flask_mux import Mux
from tests.test_mws_cases import test_mws_router


class TestMwsGet(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
