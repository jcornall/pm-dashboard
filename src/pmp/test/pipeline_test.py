import pytest
from mariadb import mariadb
from src.config.constants import MARIADB_HOST, MARIADB_PORT, MARIADB_PWD, MARIADB_USER
from src.pmp.constants import PMP_API_ABSENT_VALUE
from src.pmp.pipeline import pmp
from src.util.database import wait_for_pool_connection
from src.pmp.test.mock_allpatches_response import __MOCK_ALLPATCHES_RESPONSES
from src.pmp.test.mock_allsystems_response import __MOCK_ALLSYSTEMS_RESPONSES

__severity_enum_values = ("UNRATED", "LOW", "MODERATE", "IMPORTANT", "CRITICAL")
__resource_health_status_enum_values = (
    "UNKNOWN",
    "HEALTHY",
    "VULNERABLE",
    "HIGHLY_VULNERABLE",
)


def test_pipeline(mock_pmp_api):
    pool = mariadb.ConnectionPool(
        pool_name="pmp-pool",
        pool_size=20,
        pool_validation_interval=250,
        user=MARIADB_USER,
        password=MARIADB_PWD,
        host=MARIADB_HOST,
        port=MARIADB_PORT,
        database="pmp_test",
    )

    pmp(pool, logger=None)

    conn = wait_for_pool_connection(pool)

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT patch_id, installed_count, missing_count, severity, patch_name, patch_description, release_date FROM patches;"
        )

        all_patches = __MOCK_ALLPATCHES_RESPONSES[0]["message_response"]["allpatches"]

        for row in cursor:
            patch_info = None
            for p in all_patches:
                if int(p["patch_id"]) == row[0]:
                    patch_info = p

            if not patch_info:
                pytest.fail(f"unexpected row in 'patches' table with id P{row[0]}")

            assert row[0] == int(patch_info["patch_id"])
            assert row[1] == int(patch_info["installed"])
            assert row[2] == int(patch_info["missing"])
            assert row[3] == __severity_enum_values[int(patch_info["severity"])]
            assert row[4] == patch_info["patch_name"]
            assert row[5] == patch_info["patch_description"]

        cursor.execute(
            "SELECT resource_id, service_pack, health_status, os_platform, os_name, requires_restart FROM systems;"
        )

        all_systems = (
            __MOCK_ALLSYSTEMS_RESPONSES[0]["message_response"]["allsystems"]
            + __MOCK_ALLSYSTEMS_RESPONSES[1]["message_response"]["allsystems"]
        )

        for row in cursor:
            system_info = None
            for s in all_systems:
                if s["resource_id"] == row[0]:
                    system_info = s

            if not system_info:
                pytest.fail(f"unexpected row in 'systems' table with id P{row[0]}")

            assert row[0] == system_info["resource_id"]
            assert row[1] == system_info["service_pack"]
            assert row[2] in __resource_health_status_enum_values
            assert row[3] == system_info["os_platform_name"]
            assert row[4] == system_info["os_name"]

            if (
                system_info["resourcetorebootdetails.reboot_req_status"]
                == PMP_API_ABSENT_VALUE
            ):
                assert bool(row[5]) == False
            else:
                assert (
                    bool(row[5])
                    == system_info["resourcetorebootdetails.reboot_req_status"]
                )
