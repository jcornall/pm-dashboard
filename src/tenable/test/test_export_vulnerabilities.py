import pytest
from datetime import datetime
from dataclasses import dataclass

from src.tenable.credentials import TenableCredentials
from src.tenable.export_vulnerabilities import export_tenable_vulnerabilities

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
def post_response_success():
    return MockResponse(
        status_code=200, 
        json_data={"export_uuid": "EXPORT_UUID"}, 
        text="TEXT"
    )

@pytest.fixture(autouse=True)
def post_response_failure():
    return MockResponse(
        status_code=404, 
        json_data={"export_uuid": "EXPORT_UUID"}, 
        text="TEXT"
    )

@pytest.fixture(autouse=True)
def get_response():

    return MockResponse(
        status_code=200, 
        json_data={
            "uuid": "EXPORT_UUID",
            "chunks_failed": [],
            "chunks_cancelled": [],
            "total_chunks": 1,
            "chunks_available_count": 1,
            "empty_chunks_count": 0,
            "finished_chunks": 1,
            "filters": [],
            "num_assets_per_chunk": 100,
            "status": "FINISHED", 
            "chunks_available": [1],
            "created": int(datetime.now().timestamp())
        }, 
        text="TEXT"
    )

@pytest.fixture(autouse=True)
def mock_thread():
    return MockThread()

def test_export_tenable_vulnerabilities_success(mocker, cred_object, post_response_success, get_response, mock_thread, mock_time):
    mocker.patch("requests.post", return_value=post_response_success) 
    mocker.patch("requests.get", return_value=get_response)
    mocker.patch("threading.Thread", return_value=mock_thread)
    mocker.patch("src.tenable.export_vulnerabilities.__save_single_vuln_chunk")

    export_status = export_tenable_vulnerabilities(cred_object)
    assert export_status.uuid == "EXPORT_UUID"
    assert export_status.status == "FINISHED"
    assert export_status.chunks_available == [1]
    assert export_status.chunks_failed == []
    assert export_status.total_chunks == 1
    assert export_status.chunks_available_count == 1
    assert export_status.empty_chunks_count == 0
    assert export_status.finished_chunks == 1
    assert export_status.filters == []
    assert export_status.num_assets_per_chunk == 100
    assert export_status.created == int(mock_time)

def test_export_tenable_assets_failure(mocker, cred_object, post_response_failure):
    mocker.patch("requests.post", return_value=post_response_failure)
    with pytest.raises(RuntimeError):
        export_tenable_vulnerabilities(cred_object)

