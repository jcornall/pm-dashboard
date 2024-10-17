import pytest
import subprocess
import os
from dotenv import load_dotenv
from mariadb import mariadb
from pathlib import Path

from src.config.constants import ENV_PATH
from src.tenable.export_vulnerabilities import VulnExportStatus
from src.tenable.export_assets import AssetExportStatus
from src.tenable.load_vulnerabilities import load_tenable_vulnerabilities
from src.tenable.load_assets import load_tenable_assets


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
    "database":TEST_MARIADB_DB
}

# Test Data Filepath
# TODO: Implement pyfakefs
ASSET_EXPORT_TEST_DIR = Path(r"src") / "tenable" / "test" / "test_data" / "assets"
VULN_EXPORT_TEST_DIR = Path(r"src") / "tenable" / "test" / "test_data" / "vulnerabilities"

# DB Migrations
MIGRATION_UP = ["./golang-migrate/migrate", "-path", "./src/tenable/migrations", "-database", "mysql://test:test@tcp(localhost:3306)/testdb", "up"]
MIGRATION_DROP = ["./golang-migrate/migrate", "-path", "./src/tenable/migrations", "-database", "mysql://test:test@tcp(localhost:3306)/testdb", "drop"]


@pytest.fixture(autouse=True)
def db_migration():
    subprocess.run(MIGRATION_UP)
    yield
    subprocess.run(MIGRATION_DROP, input=b"y")

@pytest.fixture(autouse=True)
def db_connection():
    try:
        conn = mariadb.connect(**TEST_CONN_PARAMS)
        return conn
    except mariadb.Error as e:
        raise e

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
def asset_export_status():
    return AssetExportStatus(
        created=0000000000,
        uuid="TEST",
        status="FINISHED",
        chunks_available=[1]
    )

def test_load_tenable_assets_success(mocker, db_connection, vuln_export_status, asset_export_status):
    mocker.patch("src.tenable.load_assets.ASSET_EXPORT_DIR", ASSET_EXPORT_TEST_DIR)
    mocker.patch("src.tenable.load_vulnerabilities.VULN_EXPORT_DIR", VULN_EXPORT_TEST_DIR)

    load_tenable_assets(asset_export_status, db_connection)
    load_tenable_vulnerabilities(vuln_export_status, db_connection)

    try:
        db_connection.begin()
        cursor = db_connection.cursor()
        
        show_tables_statement = "SHOW TABLES;"
        cursor.execute(show_tables_statement)
        tables = cursor.fetchall()

        for table in tables:
            select_statement = f"SELECT 1 FROM {str(table).split("'")[1]} LIMIT 1"
            cursor.execute(select_statement)
            record = cursor.fetchone()
            print(str(table) + str(record))
            if record != None:
                record = record[0]
            assert record in [None, 1]

        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        raise e

