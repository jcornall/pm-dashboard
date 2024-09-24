import pytest
import os
import requests
from src.config.constants import *
from src.util.extract.asset_export import *
from unittest.mock import MagicMock

@pytest.fixture
def setup_object():
    return AssetExport()

def test_set_values(setup_object):
    test_response_json = {
        "uuid": "3faa6edf-5a06-496f-8898-2f60b32c14bf",
        "status": "FINISHED",
        "total_chunks": 1,
        "filters": "{\"tag.<category>\":\"tag.last_scan: test sf01\"}",
        "finished_chunks": 1,
        "num_assets_per_chunk": 100,
        "created": 1616117580482
    }

    setup_object.set_values(test_response_json)
    assert setup_object.uuid == test_response_json["uuid"]
    assert setup_object.total_chunks == test_response_json["total_chunks"]
    assert setup_object.filters == test_response_json["filters"]
    assert setup_object.finished_chunks == test_response_json["finished_chunks"]
    assert setup_object.num_assets_per_chunk == test_response_json["num_assets_per_chunk"]
    assert setup_object.created == test_response_json["created"]
    assert isinstance(setup_object.uuid, str) == True
    assert isinstance(setup_object.total_chunks, int) == True
    assert isinstance(setup_object.filters, str) == True
    assert isinstance(setup_object.finished_chunks, int) == True
    assert isinstance(setup_object.num_assets_per_chunk, int) == True
    assert isinstance(setup_object.created, int) == True

def test_set_status(setup_object):
    test_response_json = {
        "uuid": "3faa6edf-5a06-496f-8898-2f60b32c14bf",
        "status": "FINISHED",
        "total_chunks": 1,
        "filters": "{\"tag.<category>\":\"tag.last_scan: test sf01\"}",
        "finished_chunks": 1,
        "num_assets_per_chunk": 100,
        "created": 1616117580482
    }

    setup_object.set_status(test_response_json)
    assert setup_object.status == test_response_json["status"]
    assert isinstance(setup_object.status, str) == True

def test_set_uuid(setup_object):
    test_response_json = {
        "export_uuid": "60a26f04-c844-49a6-b67b-995a6ed79471"
    }

    setup_object.set_uuid(test_response_json)
    assert setup_object.uuid == test_response_json["export_uuid"]
    assert isinstance(setup_object.uuid, str) == True

def test_set_chunks_available(setup_object):
    test_response_json = {
        "status": "FINISHED",
        "chunks_available": [
            1,
            2,
            3,
            4
        ]
    }

    setup_object.set_chunks_available(test_response_json)
    assert setup_object.chunks_available == test_response_json["chunks_available"]
    assert isinstance(setup_object.chunks_available, list) == True

def test_log_status_code_success(setup_object, mocker):
    test_response = mocker.MagicMock()
    type(test_response).status_code = mocker.PropertyMock(return_value=200)

    result = setup_object.log_status_code(test_response)
    assert result == 0

def test_log_status_code_failure(setup_object, mocker):
    test_response = mocker.MagicMock()
    type(test_response).status_code = mocker.PropertyMock(return_value=None)

    with pytest.raises(SystemExit):
        setup_object.log_status_code(test_response)