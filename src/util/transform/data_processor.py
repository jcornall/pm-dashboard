#!/usr/bin/env python3.12
#-*- coding: utf-8 -*-
"""This module defines the DataProcessor class, used to process the raw exported JSON data into a consolidated, normalised CSV file.
"""

from src.config.transform_config import *
from pathlib import Path
import pandas as pd
import re
import json


class DataProcessor():

    def __init__(self, file_path):
        """Instantiate a DataProcessor object."""
        self.dir_path = file_path
        self.export_type = re.split("_", str(file_path))[-1]
        self.header_file = Path(RESOURCE_DIR) / f"{self.export_type}_headers.yml"

    def transform_data(self, dir_path, header_file, export_type):
        """Sequence method calls to transform the data in the supplied dir_path."""
        logging.info(f"Transforming {export_type} data...")
        purge_dir(TEMP_DIR)
        logging.info(f"Flattening {len(os.listdir(dir_path))} files...")
        for file in os.listdir(dir_path):
            json_file_path = Path(dir_path) / file
            flattened_data = self.flatten_json(json_file_path, header_file)
            self.write_json(flattened_data, file)
            # self.convert_json_to_csv(flattened_data, re.split(".", file)[0])
        self.merge_data_to_csv(export_type, header_file)
        logging.info(f"{export_type} data transformed successfully.")
        return 0

    def load_json(self, json_file_path):
        """Load the supplied JSON data file."""
        # logging.info(f"Loading {Path(json_file_path).stem}.json...")
        try:
            with open(json_file_path, encoding="utf8") as file:
                data = json.load(file)
            # logging.info(f"{Path(json_file_path).stem}.json loaded successfully.")
            return data
        except FileNotFoundError as e:
            logging.warning(f"Error: {e}. Skipping...")
        except PermissionError as e:
            logging.warning(f"Error: {e}. Skipping...")

    def flatten_json(self, json_file_path, header_file):
        """Flatten the JSON data file's nested hierarchy."""
        # logging.info(f"Flattening {Path(json_file_path).stem}.json...")
        flattened_data = []
        fields = []
        try:
            with open(header_file, "r") as file:
                config = yaml.safe_load(file)
                for key, value in config.items():
                    if value == True:
                        fields.append(key)
            # logging.info(f"Flattening items in {Path(json_file_path).stem}.json...")
            data = self.load_json(json_file_path)
            for item in data:  # Checks header_file against YAML configuration file
                flattened_item = flatten(item)
                for header in list(flattened_item):
                    if header not in fields:
                        flattened_item.pop(header)
                flattened_data.append(flattened_item)
            # logging.info(f"{Path(json_file_path).stem}.json flattened successfully.")
        except FileNotFoundError as e:
            logging.warning(f"Error: {e}. Skipping...")
        except PermissionError as e:
            logging.warning(f"Error: {e}. Skipping...")
        return flattened_data

    def write_json(self, flattened_data, file_name):
        """Write the flattened json data file to the /temp/ directory."""
        json_file = TEMP_DIR / f"{file_name}"
        # logging.info(f"Writing {file_name} flattened data to {TEMP_DIR}...")
        try:
            with open(json_file, "w") as file:
                json.dump(flattened_data, file)
            # logging.info(f"{file_name} flattened data written successfully.")
        except FileNotFoundError as e:
            logging.warning(f"Error: {e}. Skipping...")
        except PermissionError as e:
            logging.warning(f"Error: {e}. Skipping...")

    def convert_json_to_csv(self, flattened_data, file_name):
        """Convert a flattened JSON object into a CSV format."""
        csv_file = TEMP_DIR / f"{file_name}.csv"
        logging.info(f"Converting flattened {file_name} to {csv_file}...")
        df = pd.DataFrame(flattened_data)
        df.to_csv(csv_file, encoding="utf-8", index=False)
        logging.info(f"Converted {file_name} to {csv_file} successfully.")

    def merge_data_to_csv(self, export_type, header_file):
        """Merge files in the /temp/ folder into a single CSV file."""
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
        except FileNotFoundError as e:
            logging.warning(f"Error: {e}. Skipping...")
        except PermissionError as e:
            logging.warning(f"Error: {e}. Skipping...")