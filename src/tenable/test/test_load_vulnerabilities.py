import pytest
import subprocess
from mariadb import mariadb

from src.tenable.test.conftest import (
    ASSET_EXPORT_TEST_DIR,
    VULN_EXPORT_TEST_DIR,
    MIGRATION,
    TEST_MARIADB_USER,
    TEST_MARIADB_PWD,
    TEST_MARIADB_HOST,
    TEST_MARIADB_PORT,
    TEST_MARIADB_DB
)
from src.tenable.load_assets import load_tenable_assets
from src.tenable.load_vulnerabilities import load_tenable_vulnerabilities

@pytest.fixture(autouse=True)
def create_testdb():
    conn_params = {
        "user":TEST_MARIADB_USER,
        "password":TEST_MARIADB_PWD,
        "host":TEST_MARIADB_HOST,
        "port":TEST_MARIADB_PORT,
    }
    try:
        conn = mariadb.connect(**conn_params)
    except mariadb.Error as e:
        raise e

    try:
        conn.begin()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE testdb;")
        conn.commit()
        subprocess.run(MIGRATION)
    except mariadb.Error as e:
        conn.rollback()
        raise e

    yield

    try:
        conn.begin()
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE testdb;")
        conn.commit()
    except mariadb.Error as e:
        conn.rollback()
        raise e

def test_load_tenable_assets_success(mocker, export_status, vuln_export_status):
    conn_params = {
        "user":TEST_MARIADB_USER,
        "password":TEST_MARIADB_PWD,
        "host":TEST_MARIADB_HOST,
        "port":TEST_MARIADB_PORT,
        "database":TEST_MARIADB_DB
    }
    try:
        conn = mariadb.connect(**conn_params)
    except mariadb.Error as e:
        raise e

    mocker.patch("src.tenable.load_assets.ASSET_EXPORT_DIR", ASSET_EXPORT_TEST_DIR)
    mocker.patch("src.tenable.load_vulnerabilities.VULN_EXPORT_DIR", VULN_EXPORT_TEST_DIR)

    load_tenable_assets(export_status, conn)
    load_tenable_vulnerabilities(vuln_export_status, conn)

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
