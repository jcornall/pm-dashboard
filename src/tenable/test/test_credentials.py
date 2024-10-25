import pytest

def test_to_api_keys_str(tenable_credentials):
    api_keys_str = "accessKey=ACCESS_KEY;secretKey=SECRET_KEY;"
    test_keys_str = f"accessKey={tenable_credentials.access_key};secretKey={tenable_credentials.secret_key};"
    assert test_keys_str == api_keys_str
