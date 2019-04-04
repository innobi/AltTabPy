import pytest

from alt_tabpy_server.handlers import EvaluationPlaneHandler


def test_dynamic_function_building():

    def foo(arg1, arg2):
        return arg1 + arg2

    body = "return arg1 + arg2"
    kwargs = {'arg1': [10], 'arg2': [20]}
    result = EvaluationPlaneHandler._func_from_request_parts(body, kwargs)

    assert foo(**kwargs) == result(**kwargs)
