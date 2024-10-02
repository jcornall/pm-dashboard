import pytest
from unittest.mock import Mock

from src.config.constants import *
from src.tenable.credentials import *
from src.tenable.export_assets import *

@dataclass
class MockResponse:
    status_code: int
    json_data: dict
    text: str

    def json(self):
        return self.json_data

@dataclass
class MockThread:
    def start():
        pass

    def join():
        pass

@pytest.fixture(autouse=True)
def cred_object():
    return TenableCredentials(access_key="ACCESS_KEY", secret_key="SECRET_KEY")

@pytest.fixture(autouse=True)
def post_response_success():
    return MockResponse(status_code=200, json_data={"export_uuid": "EXPORT_UUID"}, text="TEXT")

@pytest.fixture(autouse=True)
def post_response_failure():
    return MockResponse(status_code=404, json_data={"export_uuid": "EXPORT_UUID"}, text="TEXT")

@pytest.fixture(autouse=True)
def get_response():
    return MockResponse(status_code=200, json_data={"status": "FINISHED", "chunks_available": [1]}, text="TEXT")

@pytest.fixture(autouse=True)
def mock_thread():
    return MockThread()

def test_export_tenable_assets_success(mocker, cred_object, post_response_success, get_response, mock_thread):
    mocker.patch("requests.post", return_value=post_response_success)
    mocker.patch("requests.get", return_value=get_response)
    mocker.patch("threading.Thread", return_value=mock_thread)
    mocker.patch("src.tenable.export_assets.__save_single_assets_chunk")
    
    export_status = export_tenable_assets(cred_object)
    assert export_status.uuid == "EXPORT_UUID"
    assert export_status.status == "FINISHED"
    assert export_status.chunks_available == [1]

def test_export_tenable_assets_failure(mocker, cred_object, post_response_failure, get_response, mock_thread):
    mocker.patch("requests.post", return_value=post_response_failure)
    with pytest.raises(RuntimeError):
        export_tenable_assets(cred_object)

