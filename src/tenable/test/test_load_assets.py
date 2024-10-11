import pytest
import subprocess
import os
from dotenv import load_dotenv
from mariadb import mariadb
from pathlib import Path

from src.config.constants import ASSET_EXPORT_DIR, ENV_PATH
from src.tenable.export_assets import AssetExportStatus
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
ASSET_EXPORT_TEST_DIR = Path(r"src") / "tenable" / "test" / "test_data" / "assets"

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
def export_status():
    return AssetExportStatus(
        created=0000000000,
        uuid="TEST",
        status="FINISHED",
        chunks_available=[1]
    )

def test_load_tenable_assets_success(mocker, db_connection, export_status):
    mocker.patch("src.tenable.load_assets.ASSET_EXPORT_DIR", ASSET_EXPORT_TEST_DIR)
    load_tenable_assets(export_status, db_connection)

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
            if record != None:
                record = record[0]
            assert record in [None, 1]

        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        raise e


