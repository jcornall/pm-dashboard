import pytest
import subprocess
from pathlib import Path
from src.tenable.pipeline import *
from src.tenable.test.conftest import TEST_ASSET_EXPORT_DIR
from src.tenable.test.conftest import (
    TEST_ASSET_EXPORT_DIR,
    TEST_VULN_EXPORT_DIR,
    TEST_MARIADB_USER,
    TEST_MARIADB_PWD,
    TEST_MARIADB_HOST,
    TEST_MARIADB_PORT,
    TEST_CONN_PARAMS,
    MIGRATION
)
from src.tenable.load_assets import load_tenable_assets

@pytest.fixture(autouse=True)
def fake_filesystem(fs):
    yield fs

@pytest.fixture(autouse=True)
def create_testdb(fs, mocker, asset_export_status):
    conn_params = {
        "user":TEST_MARIADB_USER,
        "password":TEST_MARIADB_PWD,
        "host":TEST_MARIADB_HOST,
        "port":TEST_MARIADB_PORT,
    }
    conn = mariadb.connect(**conn_params)
    conn.begin()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS testdb;")
    conn.commit()
    subprocess.run(MIGRATION)
    conn = mariadb.connect(**TEST_CONN_PARAMS)
    fs.add_real_file(TEST_ASSET_EXPORT_DIR / "0_TEST_1.json")
    mocker.patch("src.tenable.load_assets.ASSET_EXPORT_DIR", TEST_ASSET_EXPORT_DIR)
    load_tenable_assets(asset_export_status, conn)
    conn.commit()
    yield
    conn.begin()
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS testdb;")
    conn.commit()


def test_tenable_success(fs, mocker):
    mocker.patch("src.tenable.pipeline.CONN_PARAMS", TEST_CONN_PARAMS)

    fs.add_real_file(TEST_VULN_EXPORT_DIR / "0_TEST_1.json")
    fs.add_real_file(TEST_ASSET_EXPORT_DIR / "0_TEST_0.json")
    mocker.patch("src.tenable.export_vulnerabilities.VulnExportStatus.chunk_file_name", return_value="0_TEST_1.json")
    mocker.patch("src.tenable.export_assets.AssetExportStatus.chunk_file_name", return_value="0_TEST_0.json")
    mocker.patch("src.tenable.load_vulnerabilities.VULN_EXPORT_DIR", TEST_VULN_EXPORT_DIR)
    mocker.patch("src.tenable.load_assets.ASSET_EXPORT_DIR", TEST_ASSET_EXPORT_DIR)

    tenable()
