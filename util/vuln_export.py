import requests
import json
import time

class VulnExport:

    def __init__(self, response_json):
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

    def download_all_vuln_chunks(self):
        for chunk in range(1, self.total_chunks):
            self.vuln_download_chunk(chunk)
        return 0
    
    def vuln_download_chunk(self, chunk):
        print(f"Downloading chunk {chunk}")
        url = f"https://cloud.tenable.com/vulns/export/{self.uuid}/chunks/{chunk}"
        headers = {
            "accept": "application/octet-stream",
            "X-ApiKeys": "accessKey=7becc28f63abced104af4af8c52f73cd21d3d36fd771172e03eaf4ceb241964f; secretKey=37f61b104ed8983d84f38e95d1470f07c620dfc4995263933fe2a43b49acf636"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print(f"Error Code 429, retrying...")
            time.sleep(int(response.headers["Retry-After"]))
            self.vuln_download_chunk(chunk)
        else:
            response_json = json.loads(response.text)
            with open(f"{self.uuid}_{chunk}.json", "w", encoding="utf-8") as f:
                json.dump(response_json, f, ensure_ascii=False, indent=4)
            print("Download successful")
        return 0
    
    # def update_vulnexport(vuln_export):
    #     url = f"https://cloud.tenable.com/vulns/export/{vuln_export.uuid}/status"
    #     headers = {
    #         "accept": "application/json",
    #         "X-ApiKeys": "accessKey=7becc28f63abced104af4af8c52f73cd21d3d36fd771172e03eaf4ceb241964f; secretKey=37f61b104ed8983d84f38e95d1470f07c620dfc4995263933fe2a43b49acf636;"
    #     }
    #     response = requests.get(url, headers=headers)
    #     response_json = json.loads(response.text)
    #     self = 