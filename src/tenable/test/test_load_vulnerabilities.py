import pytest
import subprocess
from mariadb import mariadb

from src.tenable.test.conftest import TEST_ASSET_EXPORT_DIR, TEST_VULN_EXPORT_DIR, TEST_CONN_PARAMS, TEST_CONN_PARAMS_DB, MIGRATION
from src.tenable.load_assets import load_tenable_assets
from src.tenable.load_vulnerabilities import load_tenable_vulnerabilities

@pytest.fixture(autouse=True)
def create_testdb(fs, mocker, asset_export_status):
    conn = mariadb.connect(**TEST_CONN_PARAMS)
    conn.begin()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS testdb;")
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

def test_load_tenable_vulnerabilities_success(fs, mocker, vuln_export_status):
    fs.add_real_file(TEST_VULN_EXPORT_DIR / "0_TEST_1.json")
    mocker.patch("src.tenable.load_vulnerabilities.VULN_EXPORT_DIR", TEST_VULN_EXPORT_DIR)
    pool = mariadb.ConnectionPool(pool_name="tenable", pool_size=5, **TEST_CONN_PARAMS_DB)

    load_tenable_vulnerabilities(vuln_export_status, pool)

    conn = mariadb.connect(**TEST_CONN_PARAMS_DB)
    conn.begin()
    cursor = conn.cursor()   
    show_tables_statement = "SHOW TABLES;"
    cursor.execute(show_tables_statement)
    tables = cursor.fetchall()
    for table in tables:
        select_statement = f"SELECT 1 FROM {str(table).split("'")[1]} LIMIT 1"
        cursor.execute(select_statement)
        record = cursor.fetchone()
        if record != None:
            record = record[0]
        assert record in [None, 1]

    conn.commit()
    pool.close()

def test_load_tenable_vulnerabilities_update(fs, mocker, vuln_export_status):
    fs.add_real_file(TEST_VULN_EXPORT_DIR / "0_TEST_1.json")
    mocker.patch("src.tenable.load_vulnerabilities.VULN_EXPORT_DIR", TEST_VULN_EXPORT_DIR)
    pool = mariadb.ConnectionPool(pool_name="tenable", pool_size=5, **TEST_CONN_PARAMS_DB)

    load_tenable_vulnerabilities(vuln_export_status, pool)

    try:
        load_tenable_vulnerabilities(vuln_export_status, pool)
    except Exception as e:
        assert False, f"Error: {e}"

    pool.close()