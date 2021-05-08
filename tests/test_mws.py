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


class TestMwsPOST(FlaskMuxBaseTest):
    def setUp(self):
        super().setUp()
        self.mux.use('/', test_mws_router)

    def test_basic(self):
        """test POST method with no middlewares"""
        resp = self.client.post('/basic')
        self.assertEqual(resp.status_code, 200)

    def test_one_mw(self):
        """test POST method with one middleware"""
        body = {'message': 'samcro'}
        resp = self.client.post('/one-mw', json=body)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_one_mw_failing(self):
        """test POST method with one middleware"""
        resp = self.client.post('/one-mw')
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.json.get('success'))

    def test_multi_mws(self):
        """test POST method with multiple middleware"""
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever'}
        resp = self.client.post('/multi-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_multi_mws_failing(self):
        """test POST method with multiple middleware"""
        body = {'message': 'samcro'}
        resp = self.client.post('/multi-mws', json=body)

        self.assertEqual(resp.status_code, 401)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'unauthorized access')

    def test_extra_mws(self):
        """test POST method with many middleware"""
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever', 'admin': 'Mehdi'}
        resp = self.client.post('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('admin'), headers.get('admin'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_extra_mws_failing_1(self):
        """test POST method with many middleware"""
        body = {'message': 'samcro'}
        headers = {'admin': 'Mehdi'}
        resp = self.client.post('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 401)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'unauthorized access')

    def test_extra_mws_failing_2(self):
        """test POST method with many middleware"""
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever'}
        resp = self.client.post('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 403)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'only admins are allowed')

    def test_extra_mws_failing_3(self):
        """test POST method with many middleware"""
        headers = {'Authorization': 'whatever', 'admin': 'Mehdi'}
        resp = self.client.post('/extra-mws', headers=headers)

        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.json.get('success'))


if __name__ == '__main__':
    unittest.main()
