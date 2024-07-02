#!/usr/bin/env python3.12
#-*- coding: utf-8 -*- 

from util.config import *
import requests
import json
import time
import sys

class VulnExport:

    def __init__(self): # Instantiate VulnExport object
        pass

    def set_values(self, response_json): # Populate instance variables with request_vuln_export_status values
        self.uuid = response_json["uuid"]
        self.status = response_json["status"]
        self.chunks_available = response_json["chunks_available"]
        self.chunks_failed = response_json["chunks_failed"]
        self.chunks_cancelled = response_json["chunks_cancelled"]
        self.total_chunks = response_json["total_chunks"]
        self.chunks_available_count = response_json["chunks_available_count"]
        self.empty_chunks_count = response_json["empty_chunks_count"]
        self.finished_chunks = response_json["finished_chunks"]
        self.filters = response_json["filters"]
        self.num_assets_per_chunk = response_json["num_assets_per_chunk"]
        self.created = response_json["created"]

    def set_uuid(self, response_json):
        self.uuid = response_json["export_uuid"]

    def log_status_code(self, status_code): # Log response status codes for monitoring
        logging.info("Handling response status code...")
        match status_code:
            case 200:
                logging.info("Response Status Code 200: Request Successful.")
            case 400:
                logging.error("Response Status Code 400: Invalid Input Parameters.")
                logging.error("Exiting program...")
                sys.exit(1)
            case 403:
                logging.error("Response Status Code 403: Insufficient Permissions.")
                logging.error("Exiting program...")
                sys.exit(1)
            case 404:
                logging.error("Response Status Code 404: Resource is Missing.")
                logging.error("Exiting program...")
                sys.exit(1)
            case 409:
                logging.error("Response Status Code 409: Duplicate Request.")
                logging.error("Exiting program...")
                sys.exit(1)
            case 429:
                logging.warning("Response Status Code 429: Too Many Requests.")
            case _:
                logging.info("Unrecognised Status Code.") 
                logging.error("Exiting program...")
                sys.exit(1)

    def request_vuln_export(self): # POST call to Tenable API to export vulnerabilities
        url = "https://cloud.tenable.com/vulns/export"
        logging.info(f"POST call to {url}...")
        payload = {
            "num_assets": 50,
            "include_unlicensed": True
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-ApiKeys": f"accessKey={os.environ["TENABLE_ACCESS_KEY"]};secretKey={os.environ["TENABLE_SECRET_KEY"]};"
        }
        response = requests.post(url, json=payload, headers=headers)
        self.log_status_code(response.status_code)
        response_json = json.loads(response.text)
        self.set_uuid(response_json)
        logging.info(f"vuln_export {self.uuid} requested.")
        return 0

    def request_vuln_export_status(self): # GET call to Tenable API to update the status of the current vulnerabilities export
        url = f"https://cloud.tenable.com/vulns/export/{self.uuid}/status"
        logging.info(f"GET call to {url}...")
        headers = {
            "accept": "application/json",
            "X-ApiKeys": f"accessKey={os.environ["TENABLE_ACCESS_KEY"]};secretKey={os.environ["TENABLE_SECRET_KEY"]};"
        }
        response = requests.get(url, headers=headers)
        self.log_status_code(response.status_code)
        response_json = json.loads(response.text)
        self.set_values(response_json)
        logging.info(f"vuln_export status updated... {self.status}")
        if self.status != "FINISHED":
            logging.info(f"vuln_export {self.uuid} status: {self.status}...")
            time.sleep(10)
            self.request_vuln_export_status()
        else:
            logging.info(f"vuln_export {self.uuid} status: {self.status}.")
        return 0

    def download_all_vuln_chunks(self): # Initiate vulnerability chunk download loop
        logging.info(f"Downloading {self.total_chunks} chunks...")
        for chunk in range(1, self.total_chunks):
            self.download_vuln_chunk(chunk)
        logging.info(f"All chunks downloaded.")
        return 0

    def download_vuln_chunk(self, chunk): # GET call to Tenable API to download all vulnerability chunks
        url = f"https://cloud.tenable.com/vulns/export/{self.uuid}/chunks/{chunk}"
        logging.info(f"GET call to {url}...")
        headers = {
            "accept": "application/octet-stream",
            "X-ApiKeys": f"accessKey={os.environ["TENABLE_ACCESS_KEY"]};secretKey={os.environ["TENABLE_SECRET_KEY"]};"
        }
        response = requests.get(url, headers=headers)
        self.log_status_code(response.status_code)
        if response.status_code == 429:
            logging.warning(f"Re-attempting in {response.headers["Retry-After"]}...")
            time.sleep(int(response.headers["Retry-After"]))
            self.download_vuln_chunk(chunk)
        else:
            response_json = json.loads(response.text)
            EXPORT_DATA_FILE = VULN_EXPORT_DIR / f"{self.created}_{self.uuid}_{chunk}.json"
            with open(EXPORT_DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(response_json, f, ensure_ascii=False, indent=4)
            logging.info(f"{self.created}_{self.uuid}_{chunk}.json downloaded.")
        return 0