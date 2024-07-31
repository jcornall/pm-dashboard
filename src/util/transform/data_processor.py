from src.config.transform_config import *
from src.util.extract.api_export import APIExport
from pathlib import Path
import pandas as pd
import re
import json


class DataProcessor():

    def __init__(self, file_path):
        #  Instantiate DataProcessor objectfr
        self.dir_path = file_path
        self.export_type = re.split("_", str(file_path))[-1]
        self.header_file = Path(RESOURCE_DIR) / f"{self.export_type}_headers.yml"

    def transform_data(self, dir_path, header_file, export_type):
        #  Transform the data in the object's dir_path instance variable
        logging.info(f"Transforming {export_type} data...")
        purge_dir(TEMP_DIR)
        for file in os.listdir(dir_path):
            json_file_path = Path(dir_path) / file
            flattened_data = self.flatten_json(json_file_path, header_file)
            self.write_json(flattened_data, file)
            # self.convert_json_to_csv(flattened_data, re.split(".", file)[0])
        self.merge_data_to_csv(export_type, header_file)
        logging.info(f"{export_type} data transformed successfully.")
        return 0

    def load_json(self, json_file_path):
        #  Load a json data file
        logging.info(f"Loading {Path(json_file_path).stem}.json...")
        try:
            with open(json_file_path, encoding="utf8") as file:
                data = json.load(file)
            logging.info(f"{Path(json_file_path).stem}.json loaded successfully.")
            return data
        except FileNotFoundError:
            logging.warning(f"{Path(json_file_path).stem}.json not found. Skipping...")
        except PermissionError:
            logging.warning("Insufficient permissions. Skipping...")

    def flatten_json(self, json_file_path, header_file):
        #  Flatten the json data file's nested hierarchy
        logging.info(f"Flattening {Path(json_file_path).stem}.json...")
        flattened_data = []
        fields = []
        try:
            with open(header_file, "r") as file:
                config = yaml.safe_load(file)
                for key, value in config.items():
                    if value == True:
                        fields.append(key)
            logging.info(f"Flattening items in {Path(json_file_path).stem}.json...")
            data = self.load_json(json_file_path)
            for item in data:
                #  Checks header_file against yml configuration file
                flattened_item = flatten(item)
                for header in list(flattened_item):
                    if header not in fields:
                        flattened_item.pop(header)
                flattened_data.append(flattened_item)
            logging.info(f"{Path(json_file_path).stem}.json flattened successfully.")
        except FileNotFoundError:
            logging.warning(f"{Path(json_file_path).stem}.json not found. Skipping...")
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
        csv_file = TEMP_DIR / f"{file_name}.csv"
        logging.info(f"Converting flattened {file_name} to {csv_file}...")
        df = pd.DataFrame(flattened_data)
        df.to_csv(csv_file, encoding="utf-8", index=False)
        logging.info(f"Converted {file_name} to {csv_file} successfully.")

    def merge_data_to_csv(self, export_type, header_file):
        #  Merge files in /temp/ folder into a single csv file
        output_file = PROCESSED_DIR / f"{export_type}.csv"
        logging.info(f"Merging processed data into {Path(output_file).stem}...")
        fields = []
        try: 
            with open(header_file, "r") as file:
                config = yaml.safe_load(file)
                for key, value in config.items():
                    if value == True:
                        fields.append(key)
            logging.info(f"Loaded {header_file} successfully...")
            logging.info(f"Merging processed data into {Path(output_file).stem}.csv...")
            with open(output_file, "a", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, restval=None, fieldnames=fields, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writeheader()
                for file in os.listdir(TEMP_DIR):
                    data = self.load_json(TEMP_DIR / file)
                    for item in data:
                        writer.writerow(item)
            logging.info(f"Processed data merged into {Path(output_file).stem}.csv successfully.")
        except FileNotFoundError:
            logging.warning("File not found. Skipping...")
        except PermissionError:
            logging.warning("Insufficient permissions. Skipping...")

    """
    def validate_data():
    """