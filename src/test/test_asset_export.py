import pytest
import os
from src.config.constants import *
from src.util.extract.asset_export import *

def test_set_values(mocker):

    mock_obj = mocker.patch("src.util.extract.asset_export.AssetExport")

    test_response_json = {
        "uuid": "3faa6edf-5a06-496f-8898-2f60b32c14bf",
        "status": "FINISHED",
        "total_chunks": 1,
        "filters": "{\"tag.<category>\":\"tag.last_scan: test sf01\"}",
        "finished_chunks": 1,
        "num_assets_per_chunk": 100,
        "created": 1616117580482
    }

    mock_obj.set_values(test_response_json)
    mock_obj.set_values.assert_called_once()

    assert mock_obj.uuid == test_response_json["uuid"]
    assert mock_obj.total_chunks == test_response_json["total_chunks"]
    assert mock_obj.filters == test_response_json["filters"]
    assert mock_obj.finished_chunks == test_response_json["finished_chunks"]
    assert mock_obj.num_assets_per_chunk == test_response_json["num_assets_per_chunk"]
    assert mock_obj.created == test_response_json["created"]

    assert isinstance(mock_obj.uuid, str) == True
    assert isinstance(mock_obj.total_chunks, int) == True
    assert isinstance(mock_obj.filters, str) == True
    assert isinstance(mock_obj.finished_chunks, int) == True
    assert isinstance(mock_obj.num_assets_per_chunk, int) == True
    assert isinstance(mock_obj.created, int) == True