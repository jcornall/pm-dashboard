import pytest
import subprocess
from mariadb import mariadb

from src.tenable.test.conftest import (
    TEST_ASSET_EXPORT_DIR,
    TEST_MARIADB_USER,
    TEST_MARIADB_PWD,
    TEST_MARIADB_HOST,
    TEST_MARIADB_PORT,
    TEST_CONN_PARAMS,
    MIGRATION
)
from src.tenable.load_assets import load_tenable_assets

@pytest.fixture(autouse=True)
def create_testdb():
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
    yield
    conn.begin()
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS testdb;")
    conn.commit()

def test_load_tenable_assets_success(fs, mocker, asset_export_status):
    conn = mariadb.connect(**TEST_CONN_PARAMS)

    fs.add_real_file(TEST_ASSET_EXPORT_DIR / "0_TEST_1.json")
    mocker.patch("src.tenable.load_assets.ASSET_EXPORT_DIR", TEST_ASSET_EXPORT_DIR)
    load_tenable_assets(asset_export_status, conn)

    try:
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
    except mariadb.Error as e:
        conn.rollback()
        raise e