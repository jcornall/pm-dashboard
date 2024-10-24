import pytest
import os

from src.tenable.constants import TENABLE_API_URL
from src.tenable.export_vulnerabilities import export_tenable_vulnerabilities
from src.config.constants import VULN_EXPORT_DIR
from src.config.file_config import set_up_file_structure

@pytest.fixture(autouse=True)
def fake_filesystem(fs):
    yield fs

def test_export_tenable_vulnerabilities_success(tenable_credentials, mock_time):
    set_up_file_structure()

    export_status = export_tenable_vulnerabilities(tenable_credentials)

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


def test_export_tenable_assets_post_failure(tenable_credentials, requests_mock):
    requests_mock.post(
            f"{TENABLE_API_URL}/vulns/export", 
            status_code=403
        )

    with pytest.raises(RuntimeError):
        export_tenable_vulnerabilities(tenable_credentials)
