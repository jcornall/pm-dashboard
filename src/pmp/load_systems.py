from typing import Any
from mariadb import mariadb

from src.pmp.constants import PMP_API_ABSENT_VALUE, PMP_API_URL
from src.pmp.context import PmpPipelineContext
from src.pmp.paginate import paginate
from src.util.database import wait_for_pool_connection

__INSERT_SYSTEM_SQL = """
INSERT INTO systems(resource_id, service_pack, health_status, os_platform, os_name, requires_restart)
VALUES (?, ?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE service_pack  = ?,
                        health_status = ?,
                        os_platform   = ?,
                        os_name       = ?,
                        requires_restart = ?;
"""

__resource_health_status_enum_values = [
    "UNKNOWN",
    "HEALTHY",
    "VULNERABLE",
    "HIGHLY_VULNERABLE",
]


def load_systems(ctx: PmpPipelineContext):
    if ctx.logger:
        ctx.logger.info("loading all system data into database using 2 workers.")

    paginate(
        f"{PMP_API_URL}/api/1.4/patch/allsystems",
        headers={"Authorization": f"Bearer {ctx.access_token}"},
        on_page_fetched=__load_page_to_db,
        args=(ctx.pool,),
        max_workers=2,
    )

    if ctx.logger:
        ctx.logger.info("all system data loaded into database")


def __load_page_to_db(page: dict[str, Any], page_number: int, ctx: PmpPipelineContext):
    conn = wait_for_pool_connection(ctx.pool)
    try:
        cursor = conn.cursor()

        conn.begin()

        data = []
        for system_info in page["message_response"]["allsystems"]:
            health_status_value = system_info.get("resource_health_status")
            if not health_status_value or health_status_value == PMP_API_ABSENT_VALUE:
                health_status_value = 0

            reboot_req_status = system_info.get(
                "resourcetorebootdetails.reboot_req_status"
            )

            requires_restart = (
                reboot_req_status and reboot_req_status != PMP_API_ABSENT_VALUE
            )

            data.append(
                (
                    system_info.get("resource_id"),
                    system_info.get("service_pack"),
                    __resource_health_status_enum_values[health_status_value],
                    system_info.get("os_platform_name"),
                    system_info.get("os_name"),
                    requires_restart,
                    system_info.get("service_pack"),
                    __resource_health_status_enum_values[health_status_value],
                    system_info.get("os_platform_name"),
                    system_info.get("os_name"),
                    requires_restart,
                )
            )

        cursor.executemany(__INSERT_SYSTEM_SQL, data)

        conn.commit()
    except Exception as e:
        if ctx.logger:
            ctx.logger.error(
                f"an error occurred when loading system data to database at page {page_number}",
                e,
            )
        conn.rollback()
    finally:
        conn.close()
