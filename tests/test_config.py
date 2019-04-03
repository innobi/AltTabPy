import os
import unittest
from argparse import Namespace
from tempfile import NamedTemporaryFile

from tabpy_server.app.util import validate_cert
from tabpy_server.app.app import TabPyApp

from unittest.mock import patch, call


class TestConfigEnvironmentCalls():

    def test_no_config_file(self):
        raise NotImplementedError

    def test_no_state_ini_file_or_state_dir(self):
        raise NotImplementedError


class TestPartialConfigFile():

    def test_config_file_present(self):
        raise NotImplementedError

class TestTransferProtocolValidation():

    def test_http(self):
        raise NotImplementedError

    def test_https_without_cert_and_key(self):
        raise NotImplementedError

    def test_https_without_cert(self):
        raise NotImplementedError

    def test_https_without_key(self):
        raise NotImplementedError

    def test_https_cert_and_key_file_not_found(self):
        raise NotImplementedError

    def test_https_cert_file_not_found(self,):
        raise NotImplementedError

    def test_https_key_file_not_found(self):
        raise NotImplementedError

    def test_https_success(self):
        raise NotImplementedError

class TestCertificateValidation():

    def test_expired_cert(self):
        raise NotImplementedError        

    def test_future_cert(self):
        raise NotImplementedError        

    def test_valid_cert(self):
        raise NotImplementedError
