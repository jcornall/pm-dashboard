import pytest
from datetime import datetime
from dataclasses import dataclass

from src.tenable.pipeline import *

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

@dataclass
class MockThread:
    def start():
        pass

    def join():
        pass

@pytest.fixture(autouse=True)
def mock_thread():
    return MockThread()

def test_tenable_success(mocker, mock_thread):
    mocker.patch("mariadb.connect") 
    mocker.patch("src.config.logger_config.set_up_logger")
    mocker.patch("src.config.extract_config.purge_old_files")
    mocker.patch("src.config.extract_config.purge_empty_dirs")
    mocker.patch("src.config.extract_config.set_up_file_structure")
    mocker.patch("src.config.extract_config.set_up_dir")
    mocker.patch("src.config.extract_config.set_up_subdir")
    mocker.patch("threading.Thread", return_value=mock_thread)
    mocker.patch("src.tenable.pipeline.__process_vulnerabilities")
    mocker.patch("src.tenable.pipeline.__process_assets")

    tenable()