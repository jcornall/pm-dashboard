import pytest
import requests
import requests_mock
from datetime import datetime
from dataclasses import dataclass

from src.tenable.constants import TENABLE_API_URL
from src.tenable.credentials import TenableCredentials
from src.tenable.export_assets import export_tenable_assets

@dataclass
class MockResponse:
    # TODO: Remove once requests-mock implemented in conftest.py
    status_code: int
    json_data: dict
    text: str

    def json(self):
        return self.json_data

@dataclass
class MockThread:
    # TODO: Remove thread mocking
    def start():
        pass

    def join():
        pass

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
def post_response_failure():
    # TODO: Remove once requests-mock implemented in conftest.py
    return MockResponse(
        status_code=400, 
        json_data={"export_uuid": "EXPORT_UUID"}, 
        text="TEXT"
    )

@pytest.fixture(autouse=True)
def mock_thread():
    # TODO: Remove thread mocking
    return MockThread()

def test_export_tenable_assets_success(mocker, cred_object, requests_mock, mock_time):
    requests_mock.post(
        f"{TENABLE_API_URL}/assets/export", 
        status_code=200, 
        json_data={"export_uuid": "EXPORT_UUID"}, 
        text="TEXT",
    )

    requests_mock.get(
        f"{TENABLE_API_URL}/assets/export/{export_uuid}/status",
        status_code=200, 
        json_data={
            "status": "FINISHED", 
            "chunks_available": [1]
        }, 
        text="TEXT"
    )

    mocker.patch("requests.post", return_value=post_response_success) 
    mocker.patch("requests.get", return_value=get_response)
    # mocker.patch("src.tenable.export_assets.__save_single_assets_chunk")

    export_status = export_tenable_assets(cred_object)
    assert export_status.created == int(mock_time)
    assert export_status.uuid == "EXPORT_UUID"
    assert export_status.status == "FINISHED"
    assert export_status.chunks_available == [1]

def test_export_tenable_assets_failure(mocker, cred_object, post_response_failure):
    mocker.patch("requests.post", return_value=post_response_failure)
    with pytest.raises(RuntimeError):
        export_tenable_assets(cred_object)

