from tornado.testing import AsyncHTTPTestCase


class TestEvaluationPlainHandlerWithAuth(AsyncHTTPTestCase):

    def test_no_creds_required_auth_fails(self):
        raise NotImplementedError

    def test_invalid_creds_fails(self):
        raise NotImplementedError

    def test_valid_creds_pass(self):
        raise NotImplementedError
