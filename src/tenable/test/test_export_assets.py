import pytest
import requests
import requests_mock
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from src.tenable.constants import TENABLE_API_URL
from src.tenable.export_assets import export_tenable_assets
from src.tenable.test.conftest import ASSET_EXPORT_TEST_DIR
from src.config.constants import ASSET_EXPORT_DIR
from src.config.extract_config import set_up_file_structure

def test_export_tenable_assets_success(fake_filesystem, cred_object, requests_mock, mock_time):
    set_up_file_structure()
    requests_mock.post(
        f"{TENABLE_API_URL}/assets/export", 
        status_code=200, 
        json={"export_uuid": "EXPORT_UUID"}, 
    )

    requests_mock.get(
        f"{TENABLE_API_URL}/assets/export/EXPORT_UUID/status",
        status_code=200, 
        json={
            "status": "FINISHED", 
            "chunks_available": [1]
        }, 
    )

    fake_filesystem.pause()
    with open(ASSET_EXPORT_TEST_DIR / "0_TEST_1.json", "r") as data:
        json_string = data.read()
    fake_filesystem.resume()

    requests_mock.get(
        f"{TENABLE_API_URL}/assets/export/EXPORT_UUID/chunks/1",
        status_code=200, 
        text=json_string, 
    )

    export_status = export_tenable_assets(cred_object)
    
    assert export_status.created == int(mock_time)
    assert export_status.uuid == "EXPORT_UUID"
    assert export_status.status == "FINISHED"
    assert export_status.chunks_available == [1]

    assert os.path.exists(ASSET_EXPORT_DIR / f"{export_status.created}_{export_status.uuid}_1.json")

def test_export_tenable_assets_post_response_failure(cred_object, requests_mock):
    requests_mock.post(
        f"{TENABLE_API_URL}/assets/export", 
        status_code=403 
    )

    with pytest.raises(RuntimeError):
        export_tenable_assets(cred_object)