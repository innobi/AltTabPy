import unittest

import tornado.httputil

from alt_tabpy.handlers import EvaluateHandler


class TestEvaluateHandler(unittest.TestCase):

    def test_request_to_result(self):
        request = tornado.httputil.HTTPServerRequest(
            method='POST',
            uri='/evaluate',
            version='HTTP/1.1',
            body=(b'{"api_key":"","script":"return [x.upper() for x in '
                  b'_arg1]","data":{"_arg1":["Aaron Bergman"]}}'),
        )

        result = EvaluateHandler._request_to_result(request)
        expected = '["AARON BERGMAN"]'
        self.assertEqual(result, expected)

    def test_dynamic_function_building(self):

        def foo(arg1, arg2):
            return arg1 + arg2

        body = "return arg1 + arg2"
        kwargs = {'arg1': [10], 'arg2': [20]}
        func = EvaluateHandler._func_from_request_parts(body, kwargs)

        result = foo(**kwargs)
        expected = func(**kwargs)
        self.assertEqual(result, expected)
