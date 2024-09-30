from time import time
from mariadb import mariadb
from threading import Thread

from src.config.constants import (
    MARIADB_HOST,
    MARIADB_PORT,
    MARIADB_PWD,
    MARIADB_USER,
)
from src.pmp.auth import request_access_token
from src.pmp.load_patches import load_patches
from src.pmp.load_systems import load_systems


def pmp():
    start = time()

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

    t0 = Thread(target=load_patches, args=(pool, access_token))
    t1 = Thread(target=load_systems, args=(pool, access_token))

    t0.start()
    t1.start()

    t0.join()
    t1.join()

    end = time()

    print(f"took {end - start} seconds")
