from threading import Thread
import requests
import json
import logging
from datetime import datetime
from time import sleep
from dataclasses import dataclass
from typing import Any

from src.tenable.credentials import TenableCredentials
from src.tenable.export_status import ExportRequestStatus
from src.tenable.constants import TENABLE_API_URL
from src.config.constants import ASSET_EXPORT_DIR


@dataclass
class AssetExportStatus:
    created: int
    uuid: str
    # this stores the value of ExportRequestStatus
    status: str
    chunks_available: list[int]


def export_tenable_assets(creds: TenableCredentials):
    """
    Requests tennable to export all assets, and then saves the data into JSON files.
    This will generate multiple JSON files containing assets, as Tenable returns them in chunks.
    Each JSON file will contain a chunk of all exported assets data
    """

    api_keys = creds.to_api_keys_str()

    body = {"chunk_size": 100, "include_open_ports": False}

    response = requests.post(
        f"{TENABLE_API_URL}/assets/export",
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "X-ApiKeys": api_keys,
        },
        json=body,
    )
    if response.status_code != 200:
        msg = (
            f"assets_export failed with status {response.status_code}: {response.text}"
        )
        logging.error(msg)
        raise RuntimeError(msg)

    export_uuid = response.json()["export_uuid"]

    logging.info(f"asset_export {export_uuid} requested.")

    export_status: AssetExportStatus | None = None
    while (
        not export_status or export_status.status != ExportRequestStatus.Finished.value
    ):
        # if status previously queried, wait for 10 seconds before re-querying
        if export_status:
            sleep(10)

        url = f"{TENABLE_API_URL}/assets/export/{export_uuid}/status"
        logging.info(f"GET call to {url}...")
        status_res = requests.get(
            url,
            headers={
                "accept": "application/json",
                "X-ApiKeys": api_keys,
            },
        )
        now = datetime.now()
        export_status = AssetExportStatus(
            created=int(now.timestamp()), uuid=export_uuid, **status_res.json()
        )

        logging.info(f"asset_export {export_uuid} status: {export_status.status}...")

    threads: list[Thread] = []
    for chunk_id in export_status.chunks_available:
        t = Thread(
            target=__save_single_assets_chunk,
            args=(api_keys, export_status, chunk_id),
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def __save_single_assets_chunk(
    api_keys: str, current_export: AssetExportStatus, chunk_id: int
):
    logging.info(f"dowloading chunk {chunk_id} for asset_export {current_export.uuid}")

    should_retry = True
    res_json: Any | None = None
    while should_retry:
        response = requests.get(
            f"{TENABLE_API_URL}/assets/export/{current_export.uuid}/chunks/{chunk_id}",
            headers={"accept": "application/octet-stream", "X-ApiKeys": api_keys},
        )

        if response.status_code == 429:
            sleep(int(response.headers["Retry-After"]))
            continue

        should_retry = False
        res_json = json.loads(response.text)

    if not res_json:
        # this should not happen, but if it does something catatrophic happened
        raise RuntimeError(
            f"catatrophic failure: tenable returned an empty response when downloing chunk "
        )

    file_name = f"{current_export.created}_{current_export.uuid}_{chunk_id}.json"
    with open(ASSET_EXPORT_DIR / file_name) as f:
        json.dump(res_json, f, ensure_ascii=False, indent=4)

    logging.info(f"{file_name} downloaded.")
