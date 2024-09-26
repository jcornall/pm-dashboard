from dataclasses import dataclass
from threading import Thread
import json
import logging
from time import sleep
from typing import Any
import requests

from src.tenable.constants import TENABLE_API_URL
from src.tenable.credentials import TenableCredentials
from src.config.constants import VULN_EXPORT_DIR, VULNEXPORT_FILTER_SINCE
from src.tenable.export_status import ExportRequestStatus


@dataclass
class VulnExportStatus:
    uuid: str
    # this stores the value of ExportRequestStatus
    status: str
    chunks_available: list[int]
    chunks_failed: list[int]
    chunks_cancelled: list[int]
    total_chunks: int
    chunks_available_count: int
    empty_chunks_count: int
    finished_chunks: int
    filters: dict[str, Any]
    num_assets_per_chunk: int
    created: int

    def chunk_file_name(self, chunk_id: int) -> str:
        """Returns the name of the file that stores the data of the chunk with the given chunk id."""
        return f"{self.created}_{self.uuid}_{chunk_id}.json"


def export_tenable_vulnerabilities(creds: TenableCredentials) -> VulnExportStatus:
    """
    Requests tennable to export all vulnerabilities, and then saves the data into JSON files.
    This will generate multiple JSON files containing vulnerabilities as Tenable returns them in chunks.
    Each JSON file will contain a chunk of all exported vulnerability data
    """

    api_keys = creds.to_api_keys_str()

    body = {
        "filters": {"since": VULNEXPORT_FILTER_SINCE},
        "num_assets": 100,
        "include_unlicensed": True,
    }

    response = requests.post(
        f"{TENABLE_API_URL}/vulns/export",
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "X-ApiKeys": api_keys,
        },
        json=body,
    )
    if response.status_code != 200:
        msg = f"vuln_export failed with status {response.status_code}: {response.text}"
        logging.error(msg)
        raise RuntimeError(msg)

    export_uuid = response.json()["export_uuid"]

    logging.info(f"vuln_export {export_uuid} requested.")

    export_status: VulnExportStatus | None = None
    while (
        not export_status or export_status.status != ExportRequestStatus.Finished.value
    ):
        # if status previously queried, wait for 10 seconds before re-querying
        if export_status:
            sleep(10)

        url = f"{TENABLE_API_URL}/vulns/export/{export_uuid}/status"
        logging.info(f"GET call to {url}...")
        status_res = requests.get(
            url,
            headers={
                "accept": "application/json",
                "X-ApiKeys": api_keys,
            },
        )

        export_status = VulnExportStatus(**status_res.json())

        logging.info(f"vuln_export {export_uuid} status: {export_status.status}...")

    for chunk in export_status.chunks_available:
        # cannot multithread here because there isn't enough memory for the vm
        __save_single_vuln_chunk(api_keys, export_status, chunk)

    return export_status


def __save_single_vuln_chunk(
    api_keys: str, current_export: VulnExportStatus, chunk_id: int
):
    logging.info(
        f"downloading chunk {chunk_id} for vuln export {current_export.uuid}..."
    )

    should_retry = True
    res_json: Any | None = None
    while should_retry:
        response = requests.get(
            f"{TENABLE_API_URL}/vulns/export/{current_export.uuid}/chunks/{chunk_id}",
            headers={"accept": "application/octet-stream", "X-ApiKeys": api_keys},
        )

        if response.status_code != 200:
            retry_after = int(response.headers["Retry-After"])
            logging.warning(f"Re-attempting in {retry_after}...")
            sleep(retry_after)
            continue

        should_retry = False
        res_json = json.loads(response.text)

    if not res_json:
        # this should not happen, but if it does something catatrophic happened
        raise RuntimeError(
            f"catatrophic failure: tenable returned an empty response when downloing chunk "
        )

    file_name = current_export.chunk_file_name(chunk_id)
    with open(VULN_EXPORT_DIR / file_name, "w") as f:
        json.dump(res_json, f, ensure_ascii=False, indent=4)

    logging.info(f"{file_name} downloaded.")
