from util.vuln_export import *
# from util.asset_export import *
import logging
import requests
import json
from types import SimpleNamespace

def generate_vulnexport():
    url = "https://cloud.tenable.com/vulns/export"
    payload = {
        "num_assets": 50,
        "include_unlicensed": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-ApiKeys": "accessKey=7becc28f63abced104af4af8c52f73cd21d3d36fd771172e03eaf4ceb241964f; secretKey=37f61b104ed8983d84f38e95d1470f07c620dfc4995263933fe2a43b49acf636;"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_json = json.loads(response.text)
    export_uuid = response_json["export_uuid"]
    return 0, export_uuid

def report_vulnexport_status(export_uuid):
    url = f"https://cloud.tenable.com/vulns/export/{export_uuid}/status"
    headers = {
        "accept": "application/json",
        "X-ApiKeys": "accessKey=7becc28f63abced104af4af8c52f73cd21d3d36fd771172e03eaf4ceb241964f; secretKey=37f61b104ed8983d84f38e95d1470f07c620dfc4995263933fe2a43b49acf636;"
    }
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    vuln_export = VulnExport(response_json)
    print(f"Export {vuln_export.uuid}:" +
          f"\n - Export Status: {vuln_export.status}" +
          f"\n - Total Chunks: {vuln_export.total_chunks}")
    return vuln_export

test = report_vulnexport_status("70abb1f0-abd6-4cae-b42e-9eda2a0b8719")
test.download_all_vuln_chunks()