import pytest
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from src.config.constants import ENV_PATH
from src.tenable.constants import TENABLE_API_URL
from src.tenable.credentials import TenableCredentials
from src.tenable.export_assets import AssetExportStatus
from src.tenable.export_vulnerabilities import VulnExportStatus

# Keys
load_dotenv(dotenv_path=ENV_PATH)
TEST_MARIADB_USER = os.getenv("TEST_MARIADB_USER")
TEST_MARIADB_PWD = os.getenv("TEST_MARIADB_PWD")
TEST_MARIADB_HOST = os.getenv("TEST_MARIADB_HOST")
TEST_MARIADB_PORT = int(os.getenv("TEST_MARIADB_PORT"))
TEST_MARIADB_DB = os.getenv("TEST_MARIADB_DB")

# MariaDB Connection Parameters
TEST_CONN_PARAMS = {
    "user":TEST_MARIADB_USER,
    "password":TEST_MARIADB_PWD,
    "host":TEST_MARIADB_HOST,
    "port":TEST_MARIADB_PORT,
}

TEST_CONN_PARAMS_DB = {
    "user":TEST_MARIADB_USER,
    "password":TEST_MARIADB_PWD,
    "host":TEST_MARIADB_HOST,
    "port":TEST_MARIADB_PORT,
    "database":TEST_MARIADB_DB
}

# Test Data Filepath
TEST_ASSET_EXPORT_DIR = Path(r"src") / "tenable" / "test" / "data" / "assets"
TEST_VULN_EXPORT_DIR = Path(r"src") / "tenable" / "test" / "data" / "vulnerabilities"

# DB Migrations
MIGRATION = ["./golang-migrate/migrate", "-path", "./src/tenable/test/migrations", "-database", "mysql://test:test@tcp(localhost:3306)/testdb", "up"]

# Fixtures
@pytest.fixture(autouse=True)
def asset_export_status():
    return AssetExportStatus(
        created=0000000000,
        uuid="TEST",
        status="FINISHED",
        chunks_available=[1]
    )

@pytest.fixture(autouse=True)
def vuln_export_status():
    return VulnExportStatus(
        uuid="TEST",
        chunks_failed=[],
        chunks_cancelled=[],
        total_chunks=1,
        chunks_available_count=1,
        empty_chunks_count=0,
        finished_chunks=1,
        filters=[],
        num_assets_per_chunk=100,
        status="FINISHED",
        chunks_available=[1],
        created=0000000000,
    )

@pytest.fixture(autouse=True)
def mock_time():
    now = datetime.today()
    return now.timestamp()

@pytest.fixture(autouse=True)
def tenable_credentials():
    return TenableCredentials(
        access_key="ACCESS_KEY", 
        secret_key="SECRET_KEY"
    )

@pytest.fixture(autouse=True)
def mock_tenable_asset_responses(fs, requests_mock, mock_time):
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

    fs.pause()
    with open(TEST_ASSET_EXPORT_DIR / "0_TEST_1.json", "r") as data:
        asset_json_string = data.read()
    fs.resume()

    requests_mock.get(
        f"{TENABLE_API_URL}/vulns/export/EXPORT_UUID/chunks/1",
        status_code=200, 
        text=asset_json_string, 
    )

@pytest.fixture(autouse=True)
def mock_tenable_vuln_responses(fs, requests_mock):
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

    fs.pause()
    with open(TEST_VULN_EXPORT_DIR / "0_TEST_1.json", "r") as data:
        vuln_json_string = data.read()
    fs.resume()

    requests_mock.get(
        f"{TENABLE_API_URL}/assets/export/EXPORT_UUID/chunks/1",
        status_code=200, 
        text=vuln_json_string, 
    )