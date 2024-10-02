import pytest
import os
import subprocess

from src.config.constants import *
from src.tenable.credentials import *

@pytest.fixture(autouse=True)
def init_object():
    return TenableCredentials(access_key="ACCESS_KEY", secret_key="SECRET_KEY")

def test_to_api_keys_str(init_object):
    api_keys_str = "accessKey=ACCESS_KEY;secretKey=SECRET_KEY;"
    test_keys_str = f"accessKey={init_object.access_key};secretKey={init_object.secret_key};"
    assert test_keys_str == api_keys_str
