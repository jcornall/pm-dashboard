import pytest
import os
from datetime import datetime, timedelta

from src.config.constants import *

from src.config.extract_config import purge_empty_dirs, purge_old_files, set_up_file_structure

TEST_DIR = "tmp"

# this describes the file tree to test our functions with.
# any file path with the string "old" in it will cause mock_ctime fixture
# to return a time earlier than earliest retention date
# any file path that ends with a path separator is treated as a directory
TEST_FILE_TREE = [
    os.path.join(TEST_DIR, "old_file_0.json"),
    os.path.join(TEST_DIR, "old_file_1.json"),
    os.path.join(TEST_DIR, "new_file.json"),
    os.path.join(TEST_DIR, "old_file_2.json"),
    os.path.join(TEST_DIR, "empty") + os.path.sep,
]


@pytest.fixture(autouse=True)
def create_test_file_tree(fs):
    for path in TEST_FILE_TREE:
        if path.endswith(os.path.sep):
            fs.create_dir(path)
        else:
            fs.create_file(path)


@pytest.fixture(autouse=True)
def mock_ctime(monkeypatch):
    def __ctime(path: str):
        now = datetime.today()
        if "old" in path:
            # not the most elegant way to determine which file should
            # return a time earlier than retention date, but good enough
            old_time = now - timedelta(days=RETENTION_PERIOD + 1)
            return old_time.timestamp()
        return now.timestamp()

    monkeypatch.setattr("os.path.getctime", __ctime)


def test_set_up_file_structure():
    set_up_file_structure()

    assert os.path.exists(DATA_DIR) == True
    assert os.path.exists(VULN_DATA_DIR) == True
    assert os.path.exists(VULN_EXPORT_DIR) == True
    assert os.path.exists(ASSET_DATA_DIR) == True
    assert os.path.exists(ASSET_EXPORT_DIR) == True
    assert os.path.exists(COMPLIANCE_DATA_DIR) == True
    assert os.path.exists(COMPLIANCE_EXPORT_DIR) == True
    assert os.path.exists(TEMP_DIR) == True
    assert os.path.exists(PROCESSED_DIR) == True


def test_purge_old_files():
    purge_old_files(TEST_DIR)

    assert os.path.exists(os.path.join(TEST_DIR, "old_file_0.json")) == False
    assert os.path.exists(os.path.join(TEST_DIR, "old_file_1.json")) == False
    assert os.path.exists(os.path.join(TEST_DIR, "old_file_2.json")) == False
    assert os.path.exists(os.path.join(TEST_DIR, "new_file.json")) == True


def test_purge_empty_dirs():
    purge_empty_dirs(TEST_DIR)
    assert os.path.exists(os.path.join(TEST_DIR, "empty")) == False
