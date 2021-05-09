import unittest
from random import choice
from tests.test_base import FlaskMuxBaseTest
from tests.test_cases.test_mws import test_mws_router


class TestHandleBasic(FlaskMuxBaseTest):
    def setUp(self):
        super().setUp()
        self.mux.use('/', test_mws_router)

    def test_get(self):
        resp = self.client.get('/handle-basic')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), 'GET')

    def test_post(self):
        resp = self.client.post('/handle-basic')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), 'POST')

    def test_put(self):
        resp = self.client.put('/handle-basic')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), 'PUT')

    def test_delete(self):
        resp = self.client.delete('/handle-basic')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), 'DELETE')


class TestHandleWithMiddlewares(FlaskMuxBaseTest):
    def setUp(self):
        super().setUp()
        self.mux.use('/', test_mws_router)

    def test_one_mw(self):
        """"""
        # select HTTP method randomly
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        headers = {'Authorization': 'whatever'}
        resp = http_func('/handle-one-mw', headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), method)

    def test_one_mw_failing(self):
        """"""
        # select HTTP method randomly
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        resp = http_func('/handle-one-mw')

        self.assertEqual(resp.status_code, 401)

    def test_multi_mws(self):
        """"""
        # select HTTP method randomly
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        headers = {'Authorization': 'whatever'}
        body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
        resp = http_func('/handle-multi-mws', headers=headers, json=body)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), method)
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_multi_mws_failing_1(self):
        """"""
        # select HTTP method randomly
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        headers = {'Authorization': 'whatever'}
        resp = http_func('/handle-multi-mws', headers=headers)

        self.assertEqual(resp.status_code, 400)

    def test_multi_mws_failing_2(self):
        """"""
        # select HTTP method randomly
        methods = ['POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
        resp = http_func('/handle-multi-mws', json=body)

        self.assertEqual(resp.status_code, 401)

    def test_extra_mws(self):
        """"""
        # select HTTP method randomly
        methods = ['POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        admin = 'mehdi'
        headers = {'Authorization': 'whatever', 'admin': admin}
        body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
        resp = http_func('/handle-extra-mws', headers=headers, json=body)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json.get('method'), method)
        self.assertEqual(resp.json.get('admin'), admin)
        self.assertDictEqual(resp.json.get('req_body'), body)

    def test_extra_mws_failing_1(self):
        """"""
        # select HTTP method randomly
        methods = ['POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        headers = {'Authorization': 'whatever', 'admin': 'mehdi'}
        resp = http_func('/handle-extra-mws', headers=headers)

        self.assertEqual(resp.status_code, 400)

    def test_extra_mws_failing_2(self):
        """"""
        # select HTTP method randomly
        methods = ['POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        headers = {'Authorization': 'whatever'}
        body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
        resp = http_func('/handle-extra-mws', headers=headers, json=body)

        self.assertEqual(resp.status_code, 403)

    def test_extra_mws_failing_3(self):
        """"""
        # select HTTP method randomly
        methods = ['POST', 'PUT', 'DELETE']
        method = choice(methods)

        http_func = getattr(self.client, method.lower())
        headers = {'admin': 'mehdi'}
        body = {'message': 'BEARS. BEETS. BATTLESTAR GALACTICA.'}
        resp = http_func('/handle-extra-mws', headers=headers, json=body)

        self.assertEqual(resp.status_code, 401)


if __name__ == '__main__':
    unittest.main()
