import pytest
import subprocess
from pathlib import Path
from mariadb import mariadb

from src.tenable.pipeline import *
from src.tenable.test.conftest import TEST_ASSET_EXPORT_DIR
from src.tenable.test.conftest import TEST_ASSET_EXPORT_DIR, TEST_VULN_EXPORT_DIR, TEST_CONN_PARAMS, TEST_CONN_PARAMS_DB, MIGRATION
from src.tenable.load_assets import load_tenable_assets

@pytest.fixture(autouse=True)
def fake_filesystem(fs):
    yield fs

@pytest.fixture(autouse=True)
def create_testdb(fs, mocker, asset_export_status):
    conn = mariadb.connect(**TEST_CONN_PARAMS)
    conn.begin()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS tenable;")
    conn.commit()

    subprocess.run(MIGRATION)

    conn = mariadb.connect(**TEST_CONN_PARAMS_DB)
    fs.add_real_file(TEST_ASSET_EXPORT_DIR / "0_TEST_1.json")  # Test asset data is loaded early so that load_vulnerabilities can reference asset_uuids as a foreign key
    mocker.patch("src.tenable.load_assets.ASSET_EXPORT_DIR", TEST_ASSET_EXPORT_DIR)
    pool = mariadb.ConnectionPool(pool_name="tenable", pool_size=5, **TEST_CONN_PARAMS_DB)

    load_tenable_assets(asset_export_status, pool)

    conn.commit()
    pool.close()

    yield

    conn.begin()
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS testdb;")
    conn.commit()


def test_tenable_success(fs, mocker):
    pool = mariadb.ConnectionPool(pool_name="tenable", pool_size=5, **TEST_CONN_PARAMS_DB)
    mocker.patch("mariadb.ConnectionPool", return_value=pool)
    fs.add_real_file(TEST_VULN_EXPORT_DIR / "0_TEST_1.json")
    fs.add_real_file(TEST_ASSET_EXPORT_DIR / "0_TEST_0.json")  # Alternate test asset data is loaded to avoid duplication
    mocker.patch("src.tenable.export_vulnerabilities.VulnExportStatus.chunk_file_name", return_value="0_TEST_1.json")
    mocker.patch("src.tenable.export_assets.AssetExportStatus.chunk_file_name", return_value="0_TEST_0.json")
    mocker.patch("src.tenable.load_vulnerabilities.VULN_EXPORT_DIR", TEST_VULN_EXPORT_DIR)
    mocker.patch("src.tenable.load_assets.ASSET_EXPORT_DIR", TEST_ASSET_EXPORT_DIR)

    tenable()
