from src.config.transform_config import *
from src.util.extract.api_export import APIExport
from pathlib import Path
import pandas as pd
import re
import json


class DataProcessor():

    def __init__(self, file_path): 
        #  Instantiate DataProcessor object
        self.dir_path = file_path
        self.export_type = re.split("_", str(file_path))[-1]
        self.headers = Path(RESOURCE_DIR) / f"{self.export_type}_headers.yml"

    def transform_data(self):
        #  Transform the data in the object's dir_path instance variable
        logging.info("Handling response status code...")
        purge_temp()
        for file in os.listdir(self.dir_path):
            flattened_data = self.flatten_json(self.load_json(Path(self.dir_path) / file), self.headers)
            self.write_json(flattened_data, file)
            # self.convert_json_to_csv(flattened_data, re.split(".", file)[0])
        self.merge_data_to_csv()
        return 0

    def load_json(self, json_file):
        #  Load a json data file
        logging.info(f"Loading {json_file}...")
        try:
            with open(json_file, encoding="utf8") as file:
                data = json.load(file)
            logging.info(f"{json_file} loaded successfully.")
        except FileNotFoundError:
            logging.warning(f"{json_file} not found. Skipping...")
        except PermissionError:
            logging.warning("Insufficient permissions. Skipping...")
        return data

    def flatten_json(self, json_file, headers):
        #  Flatten the json data file's nested hierarchy
        logging.info(f"Flattening json file...")
        flattened_data = []
        try:
            with open(headers, "r") as file:
                config = yaml.safe_load(file)
            for item in json_file:
                #  Checks headers against yml configuration file
                for header in list(item):
                    if (header in config and config[header] == False):
                        item.pop(header)
                flattened_item = flatten(item)
                flattened_data.append(flattened_item)
            logging.info(f"json file flattened successfully.")
        except FileNotFoundError:
            logging.warning("File not found. Skipping...")
        except PermissionError:
            logging.warning("Insufficient permissions. Skipping...")
        return flattened_data

    def write_json(self, flattened_data, file_name):
        #  Write the flattened json data file to the /temp/ directory
        logging.info(f"Writing {file_name} flattened data to {TEMP_DIR}...")
        try:
            with open(TEMP_DIR / file_name, "w") as file:
                json.dump(flattened_data, file)
            logging.info(f"{file_name} flattened data written successfully.")
        except FileNotFoundError:
            logging.warning("File not found. Skipping...")
        except PermissionError:
            logging.warning("Insufficient permissions. Skipping...")

    def convert_json_to_csv(self, flattened_data, file_name):
        #  Convert a flattened json object into a csv format
        csv_file = f"{file_name}.csv"
        logging.info(f"Converting flattened {file_name} to {csv_file}...")
        df = pd.DataFrame(flattened_data)
        df.to_csv(TEMP_DIR / csv_file, encoding="utf-8", index=False)
        logging.info(f"Converted {file_name} to {csv_file} successfully.")

    """
    def validate_data():
    """

    def merge_data_to_csv(self):
        #  Merge files in /temp/ folder into a single csv file
        with open(self.headers, "r") as file:
                config = yaml.safe_load(file)
                fields = config.keys()
        with open(f"{self.export_type}.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, restval=None, fieldnames=fields)
            writer.writeheader()
            for file in os.listdir(TEMP_DIR):
                for item in file:
                    writer.writerow(item)