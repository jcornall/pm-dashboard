import pytest
import requests
import requests_mock
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from src.tenable.constants import TENABLE_API_URL
from src.tenable.credentials import TenableCredentials
from src.tenable.export_assets import export_tenable_assets
from src.tenable.test.conftest import ASSET_EXPORT_TEST_DIR
from src.config.constants import ASSET_EXPORT_DIR
from src.config.extract_config import set_up_file_structure

@pytest.fixture(autouse=True)
def mock_time():
    now = datetime.today()
    return now.timestamp()

@pytest.fixture(autouse=True)
def cred_object():
    return TenableCredentials(
        access_key="ACCESS_KEY", 
        secret_key="SECRET_KEY"
    )

@pytest.fixture(autouse=True)
def fake_filesystem(fs):
    yield fs

def test_export_tenable_assets_success(fake_filesystem, cred_object, requests_mock, mock_time):
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

    set_up_file_structure()

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

# def test_export_tenable_assets_get_response_failure(cred_object, requests_mock, mock_time):
#     requests_mock.post(
#         f"{TENABLE_API_URL}/assets/export", 
#         status_code=200, 
#         json={"export_uuid": "EXPORT_UUID"}, 
#     )

#     requests_mock.get(
#         f"{TENABLE_API_URL}/assets/export/EXPORT_UUID/status",
#         status_code=403
#     )

#     with pytest.raises(RuntimeError):
#         export_tenable_assets(cred_object)