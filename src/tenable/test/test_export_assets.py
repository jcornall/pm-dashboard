import pytest
import os

from src.tenable.constants import TENABLE_API_URL
from src.tenable.export_assets import export_tenable_assets
from src.config.constants import ASSET_EXPORT_DIR
from src.config.file_config import set_up_file_structure

@pytest.fixture(autouse=True)
def fake_filesystem(fs):
    yield fs

def test_export_tenable_assets_success(tenable_credentials, mock_time):
    set_up_file_structure()

    export_status = export_tenable_assets(tenable_credentials)

    assert export_status.created == int(mock_time)
    assert export_status.uuid == "EXPORT_UUID"
    assert export_status.status == "FINISHED"
    assert export_status.chunks_available == [1]

    assert os.path.exists(ASSET_EXPORT_DIR / f"{export_status.created}_{export_status.uuid}_1.json")

def test_export_tenable_assets_post_response_failure(tenable_credentials, requests_mock):
    requests_mock.post(
        f"{TENABLE_API_URL}/assets/export", 
        status_code=403 
    )

    with pytest.raises(RuntimeError):
        export_tenable_assets(tenable_credentials)
