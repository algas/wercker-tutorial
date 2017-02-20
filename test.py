import app

from tornado.testing import AsyncHTTPTestCase, gen_test
import tornado
import logging
import unittest
import json

class ApiTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return app.Application()

    @gen_test(timeout=10)
    def test_helloworld(self):
        response = yield self.http_client.fetch(self.get_url('/'))
        self.assertEqual(response.body.decode('utf-8'), "Hello, world")

    @gen_test(timeout=10)
    def test_user(self):
        response = yield self.http_client.fetch(self.get_url('/users/1'))
        self.assertEqual(json.loads(response.body.decode('utf-8')), [{"id":1, "name":"foo"}])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
