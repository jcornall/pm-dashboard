from math import ceil
from typing import Any
import requests
from mariadb import mariadb
from concurrent.futures.thread import ThreadPoolExecutor

from src.pmp.constants import PMP_API_ABSENT_VALUE, PMP_API_URL
from src.pmp.exceptions import UnexpectedApiResponse
from src.util.database import wait_for_pool_connection

__INSERT_SYSTEM_SQL = """
INSERT INTO systems(resource_id, service_pack, health_status, os_platform, os_name)
VALUES (?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE service_pack  = ?,
                        health_status = ?,
                        os_platform   = ?,
                        os_name       = ?;
"""

__resource_health_status_enum_values = [
    "UNKNOWN",
    "HEALTHY",
    "VULNERABLE",
    "HIGHLY_VULNERABLE",
]


def load_systems(pool: mariadb.ConnectionPool, access_token: str):
    # page index starts from 1 instead of 0

    first_page = __fetch_single_page(page=1, access_token=access_token)

    total_pages = ceil(
        first_page["message_response"]["total"]
        / first_page["message_response"]["limit"]
    )

    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.submit(__load_page_to_db, first_page, pool)

        # since the first page is already fetched, we need to fetch one less page
        for i in range(total_pages - 1):
            # i is zero-based, so +1 to make it one-based, and another +1 to skip the first page
            executor.submit(__fetch_and_load_page, i + 2, pool, access_token)


def __fetch_and_load_page(page: int, pool: mariadb.ConnectionPool, access_token: str):
    print("fetching page", page)
    page_json = __fetch_single_page(page, access_token)
    __load_page_to_db(page_json, pool)
    print(f"page {page} loaded")


def __fetch_single_page(page: int, access_token: str):
    res = requests.get(
        f"{PMP_API_URL}/api/1.4/patch/allsystems?page={page}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        return res.json()
    except KeyError:
        raise UnexpectedApiResponse()


def __load_page_to_db(page: dict[str, Any], pool: mariadb.ConnectionPool):
    conn = wait_for_pool_connection(pool)
    try:
        cursor = conn.cursor()

        conn.begin()

        data = []
        for system_info in page["message_response"]["allsystems"]:
            health_status_value = system_info.get("resource_health_status")
            if not health_status_value or health_status_value == PMP_API_ABSENT_VALUE:
                health_status_value = 0
            data.append(
                (
                    system_info.get("resource_id"),
                    system_info.get("service_pack"),
                    __resource_health_status_enum_values[health_status_value],
                    system_info.get("os_platform_name"),
                    system_info.get("os_name"),
                    system_info.get("service_pack"),
                    __resource_health_status_enum_values[health_status_value],
                    system_info.get("os_platform_name"),
                    system_info.get("os_name"),
                )
            )

        cursor.executemany(__INSERT_SYSTEM_SQL, data)
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
