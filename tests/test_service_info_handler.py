from tornado.testing import AsyncHTTPTestCase


class TestServiceInfoHandlerDefault(AsyncHTTPTestCase):

    def test_given_vanilla_tabpy_server_expect_correct_info_response(self):
        raise NotImplementedError

class TestServiceInfoHandlerWithAuth(AsyncHTTPTestCase):

    def test_given_tabpy_server_with_auth_expect_correct_info_response(self):
        raise NotImplementedError
