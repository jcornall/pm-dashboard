from typing import Any
from mariadb import mariadb

from src.pmp.constants import PMP_API_URL
from src.pmp.paginate import paginate
from src.util.database import wait_for_pool_connection

__INSERT_PATCH_SQL = """
INSERT INTO patches(patch_id, installed_count, missing_count, severity, patch_name, patch_description)
VALUES (?, ?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE installed_count   = ?,
                        missing_count     = ?,
                        severity          = ?,
                        patch_name        = ?,
                        patch_description = ?;
"""

__severity_enum_values = ("UNRATED", "LOW", "MODERATE", "IMPORTANT", "CRITICAL")


def load_patches(pool: mariadb.ConnectionPool, access_token: str):
    paginate(
        f"{PMP_API_URL}/api/1.4/patch/allpatches",
        headers={"Authorization": f"Bearer {access_token}"},
        on_page_fetched=__load_page_to_db,
        args=(pool,),
        max_workers=10,
    )


def __load_page_to_db(
    page: dict[str, Any], page_number: int, pool: mariadb.ConnectionPool
):
    print(f"loading patch page {page_number}...")

    conn = wait_for_pool_connection(pool)
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
                int(patch.get("installed")),
                int(patch.get("missing")),
                __severity_enum_values[int(patch.get("severity"))],
                patch.get("patch_name"),
                patch.get("patch_description"),
            )
            for patch in page["message_response"]["allpatches"]
        ]

        cursor.executemany(__INSERT_PATCH_SQL, data)

        conn.commit()

        print(f"patch page {page_number} loaded")
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
