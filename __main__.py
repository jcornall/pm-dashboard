from util.vuln_export import *
# from util.asset_export import *
import logging
import requests
import os
import json
import logging
import datetime

current_time = datetime.current_time()
logging.basicConfig(filename=f"{current_time.strftime("%Y%m%d_%H%M%S")}.log", filemode="w", format="%(asctime)s:%(name)s:%(levelname)s - %(message)s")

def request_vuln_export():
    url = "https://cloud.tenable.com/vulns/export"
    payload = {
        "num_assets": 50,
        "include_unlicensed": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-ApiKeys": f"accessKey={os.environ["TENABLE_ACCESS_KEY"]}; secretKey={os.environ["TENABLE_SECRET_KEY"]};"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_json = json.loads(response.text)
    export_uuid = response_json["export_uuid"]
    return 0, export_uuid

def request_vuln_export_status(export_uuid):
    url = f"https://cloud.tenable.com/vulns/export/{export_uuid}/status"
    headers = {
        "accept": "application/json",
        "X-ApiKeys": f"accessKey={os.environ["TENABLE_ACCESS_KEY"]}; secretKey={os.environ["TENABLE_SECRET_KEY"]};"
    }
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    vuln_export = VulnExport(response_json)
    print(f"Export {vuln_export.uuid}:" +
          f"\n - Export Status: {vuln_export.status}" +
          f"\n - Total Chunks: {vuln_export.total_chunks}")
    return vuln_export

def check_data_folder():
    print("Checking if /pmt-dashboard/data/ exists...")
    if os.path.isdir("./data/"):
        print("Directory exists.")
    else:
        print("Directory does not exist, creating directory...")
        os.mkdir("data")
        print("Directory created.")