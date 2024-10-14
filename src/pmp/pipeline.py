import logging
from os import makedirs
from mariadb import mariadb
from threading import Thread

from src.config.constants import (
    EXPORT_LOG_DIR,
    FORMATTED_DATE,
    FORMATTED_TIME,
    MARIADB_HOST,
    MARIADB_PORT,
    MARIADB_PWD,
    MARIADB_USER,
)
from src.pmp.auth import request_access_token
from src.pmp.context import PmpPipelineContext
from src.pmp.load_patches import load_patches
from src.pmp.load_systems import load_systems


def __setup_logging():
    logger = logging.getLogger("pmp_logger")
    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(module)s:%(levelname)s - %(message)s"
    )

    makedirs(EXPORT_LOG_DIR / "pmp", exist_ok=True)
    file_handler = logging.FileHandler(
        EXPORT_LOG_DIR / "pmp" / f"{FORMATTED_DATE}_{FORMATTED_TIME}.log", mode="w"
    )
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger


def pmp(
    pool: mariadb.ConnectionPool | None = None,
    logger: logging.Logger | None = __setup_logging(),
):
    access_token = request_access_token()

    if not pool:
        pool = mariadb.ConnectionPool(
            pool_name="pmp-pool",
            pool_size=20,
            pool_validation_interval=250,
            user=MARIADB_USER,
            password=MARIADB_PWD,
            host=MARIADB_HOST,
            port=MARIADB_PORT,
            database="patch_manager_plus",
        )

    ctx = PmpPipelineContext(pool, access_token, logger)

    t0 = Thread(target=load_patches, args=(ctx,))
    t1 = Thread(target=load_systems, args=(ctx,))

    t0.start()
    t1.start()

    t0.join()
    t1.join()
