import pytest
import os

__FAKE_ENV = {"MARIADB_PORT": 4321}


for key, val in __FAKE_ENV.items():
    os.environ[key] = str(val)
