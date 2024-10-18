import pytest
import requests
import requests_mock
import os

from src.tenable.constants import TENABLE_API_URL
from src.tenable.export_vulnerabilities import export_tenable_vulnerabilities
from src.tenable.test.conftest import VULN_EXPORT_TEST_DIR
from src.config.constants import VULN_EXPORT_DIR
from src.config.extract_config import set_up_file_structure

@pytest.fixture(autouse=True)
def fake_filesystem(fs):
    yield fs

def test_export_tenable_vulnerabilities_success(fake_filesystem, cred_object, requests_mock, mock_time):
    set_up_file_structure()
    requests_mock.post(
        f"{TENABLE_API_URL}/vulns/export", 
        status_code=200, 
        json={"export_uuid": "EXPORT_UUID"}, 
    )

    requests_mock.get(
        f"{TENABLE_API_URL}/vulns/export/EXPORT_UUID/status",
        status_code=200, 
        json={
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
            "created": int(mock_time)
        }, 
    )

    fake_filesystem.pause()
    with open(VULN_EXPORT_TEST_DIR / "0_TEST_1.json", "r") as data:
        json_string = data.read()
    fake_filesystem.resume()

    requests_mock.get(
        f"{TENABLE_API_URL}/vulns/export/EXPORT_UUID/chunks/1",
        status_code=200, 
        text=json_string, 
    )

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

    assert os.path.exists(VULN_EXPORT_DIR / f"{export_status.created}_{export_status.uuid}_1.json")


def test_export_tenable_assets_post_failure(cred_object, requests_mock):
    requests_mock.post(
            f"{TENABLE_API_URL}/vulns/export", 
            status_code=403 
        )

    with pytest.raises(RuntimeError):
        export_tenable_vulnerabilities(cred_object)
