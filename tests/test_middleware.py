"""
Filename: test_middleware.py
Author: George Deamont <deamontg@gmail.com>
Description: Middleware tests.
"""

import falcon, json

from falcon import testing

from app.middleware import JSONBodyParser


class MiddlewareTestCase(testing.TestCase):
    """
    """
    
    def test_json_body_parser_middleware_with_valid_json(self):
        """
        """
        data = {'valid': 'json'}
        environ = testing.create_environ(method='POST', body=json.dumps(data))
        req = falcon.Request(environ)
        resp = falcon.Response()
        middleware = JSONBodyParser()
        middleware.process_request(req, resp)

        self.assertEqual(req.context['data'], data)


    def test_json_body_parser_middleware_with_invalid_json_1(self):
        """
        """
        data = 'Invalid JSON'
        environ = testing.create_environ(method='POST', body=json.dumps(data))
        req = falcon.Request(environ)
        resp = falcon.Response()
        middleware = JSONBodyParser()
        
        with self.assertRaises(falcon.HTTPBadRequest):
            middleware.process_request(req, resp)


    def test_json_body_parser_middleware_with_invalid_json_2(self):
        """
        """
        data = None
        environ = testing.create_environ(method='POST', body=json.dumps(data))
        req = falcon.Request(environ)
        resp = falcon.Response()
        middleware = JSONBodyParser()
        
        with self.assertRaises(falcon.HTTPBadRequest):
            middleware.process_request(req, resp)