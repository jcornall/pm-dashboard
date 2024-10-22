import pytest
import requests
import requests_mock
import os

from src.tenable.constants import TENABLE_API_URL
from src.tenable.export_assets import export_tenable_assets
from src.tenable.test.conftest import TEST_ASSET_EXPORT_DIR
from src.config.constants import ASSET_EXPORT_DIR
from src.config.extract_config import set_up_file_structure

@pytest.fixture(autouse=True)
def fake_filesystem(fs):
    yield fs

def test_export_tenable_assets_success(fs, cred_object, requests_mock, mock_time):
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
