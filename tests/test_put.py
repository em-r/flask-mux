import unittest
from tests.test_base import FlaskMuxBaseTest
from tests.test_cases.test_mws import test_mws_router


class TestMwsPUT(FlaskMuxBaseTest):
    def setUp(self):
        super().setUp()
        self.mux.use('/', test_mws_router)
        self.req_func = self.client.put

    def test_basic(self):
        """test PUT method with no middlewares"""
        resp = self.req_func('/basic')
        self.assertEqual(resp.status_code, 200)

    def test_one_mw(self):
        """test PUT method with one middleware"""
        body = {'message': 'samcro'}
        resp = self.req_func('/one-mw', json=body)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_one_mw_failing(self):
        """test PUT method with one middleware"""
        resp = self.req_func('/one-mw')
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.json.get('success'))

    def test_multi_mws(self):
        """test PUT method with multiple middleware"""
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever'}
        resp = self.req_func('/multi-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_multi_mws_failing(self):
        """test PUT method with multiple middleware"""
        body = {'message': 'samcro'}
        resp = self.req_func('/multi-mws', json=body)

        self.assertEqual(resp.status_code, 401)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'unauthorized access')

    def test_extra_mws(self):
        """test PUT method with many middleware"""
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever', 'admin': 'Mehdi'}
        resp = self.req_func('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json.get('success'))
        self.assertEqual(resp.json.get('admin'), headers.get('admin'))
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_extra_mws_failing_1(self):
        """test PUT method with many middleware"""
        body = {'message': 'samcro'}
        headers = {'admin': 'Mehdi'}
        resp = self.req_func('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 401)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'unauthorized access')

    def test_extra_mws_failing_2(self):
        """test PUT method with many middleware"""
        body = {'message': 'samcro'}
        headers = {'Authorization': 'whatever'}
        resp = self.req_func('/extra-mws', json=body, headers=headers)

        self.assertEqual(resp.status_code, 403)
        self.assertFalse(resp.json.get('success'))
        self.assertEqual(resp.json.get('message'), 'only admins are allowed')

    def test_extra_mws_failing_3(self):
        """test PUT method with many middleware"""
        headers = {'Authorization': 'whatever', 'admin': 'Mehdi'}
        resp = self.req_func('/extra-mws', headers=headers)

        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.json.get('success'))


if __name__ == '__main__':
    unittest.main()
