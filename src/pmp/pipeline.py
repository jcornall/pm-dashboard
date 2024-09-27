from mariadb import mariadb

from src.config.constants import (
    MARIADB_DB,
    MARIADB_HOST,
    MARIADB_PORT,
    MARIADB_PWD,
    MARIADB_USER,
)
from src.pmp.auth import request_access_token
from src.pmp.load_systems import load_systems


def pmp():
    access_token = request_access_token()

    pool = mariadb.ConnectionPool(
        user=MARIADB_USER,
        password=MARIADB_PWD,
        host=MARIADB_HOST,
        port=MARIADB_PORT,
        database="patch_manager_plus",
        pool_name="pmp-pool",
        pool_size=20,
        pool_validation_interval=250,
    )

    load_systems(pool, access_token)
