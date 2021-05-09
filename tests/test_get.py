import unittest
from tests.test_base import FlaskMuxBaseTest
from tests.test_cases.test_mws import test_mws_router


class TestMwsGET(FlaskMuxBaseTest):
    def setUp(self):
        super().setUp()
        self.mux.use('/', test_mws_router)

    def test_basic(self):
        """test GET method with no middlewares"""
        resp = self.client.get('/basic')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))

    def test_one_mw(self):
        """test GET method with one middlewares"""
        headers = {'admin': 'Mehdi'}
        resp = self.client.get('/get-with-auth', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('admin'), headers.get('admin'))

    def test_one_mw_failing(self):
        """test GET method with one middlewares"""
        resp = self.client.get('/get-with-auth')
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(resp.json.get('success'))

    def test_multi_mws(self):
        """test GET method with multiple middlewares"""
        headers = {
            'Authorization': 'whatever',
            'admin': 'Mehdi'
        }
        resp = self.client.get('/get-with-multi-mws', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('admin'), headers.get('admin'))

    def test_multi_mws_failing(self):
        """test GET method with multiple middlewares"""
        resp = self.client.get('/get-with-auth')
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(resp.json.get('success'))

    def test_extra_mws(self):
        """test GET method with many middlewares"""
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
