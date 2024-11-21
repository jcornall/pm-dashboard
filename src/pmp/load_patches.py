from typing import Any
from mariadb import mariadb

from src.pmp.constants import PMP_API_URL
from src.pmp.context import PmpPipelineContext
from src.pmp.paginate import paginate
from src.util.database import wait_for_pool_connection

__INSERT_PATCH_SQL = """
INSERT INTO patches(patch_id, installed_count, missing_count, severity, patch_name, patch_description, release_date)
VALUES (?, ?, ?, ?, ?, ?, FROM_UNIXTIME(? / 1000))
ON DUPLICATE KEY UPDATE installed_count   = ?,
                        missing_count     = ?,
                        severity          = ?,
                        patch_name        = ?,
                        patch_description = ?,
                        release_date = FROM_UNIXTIME(? / 1000);
"""

__severity_enum_values = ("UNRATED", "LOW", "MODERATE", "IMPORTANT", "CRITICAL")


def load_patches(ctx: PmpPipelineContext):
    if ctx.logger:
        ctx.logger.info("loading patch data to database")

    paginate(
        f"{PMP_API_URL}/api/1.4/patch/allpatches",
        headers={"Authorization": f"Bearer {ctx.access_token}"},
        on_page_fetched=__load_page_to_db,
        args=(ctx,),
        max_workers=2,
    )

    if ctx.logger:
        ctx.logger.info("all patch data loaded into database.")


def __load_page_to_db(
    page: dict[str, Any],
    page_number: int,
    ctx: PmpPipelineContext,
):
    conn = wait_for_pool_connection(ctx.pool)
    cursor = conn.cursor()

    try:
        conn.begin()

        data = [
            (
                int(patch.get("patch_id")),
                int(patch.get("installed")),
                int(patch.get("missing")),
                __severity_enum_values[int(patch.get("severity"))],
                patch.get("patch_name"),
                patch.get("patch_description"),
                int(patch.get("patch_released_time")),
                int(patch.get("installed")),
                int(patch.get("missing")),
                __severity_enum_values[int(patch.get("severity"))],
                patch.get("patch_name"),
                patch.get("patch_description"),
                int(patch.get("patch_released_time")),
            )
            for patch in page["message_response"]["allpatches"]
        ]

        cursor.executemany(__INSERT_PATCH_SQL, data)

        conn.commit()
    except Exception as e:
        if ctx.logger:
            ctx.logger.error(
                f"an error occurred when loading patch data to database at page {page_number}",
                e,
            )
        conn.rollback()
    finally:
        conn.close()
