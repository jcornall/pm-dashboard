from src.config.extract_config import *
from src.config.constants import *
import json
import csv
import yaml
import os
from flatten_json import flatten

def load_json(json_file):
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

def dump_headers_to_yaml(headers, export_type):
    #  Dumps list of headers to a yaml resource file
    yml_file = f"{export_type}_headers.yml"
    logging.info(f"Dumping json headers to {yml_file}...")
    headers = dict(sorted(headers.items(), key=lambda x:x[1]))
    try:
        with open(Path(RESOURCE_DIR) / f"{yml_file}", "w") as file:
            yaml.dump(headers, file, default_flow_style=False)
        logging.info(f"Headers dumped to {export_type}_headers.yml successfully.")
    except:
        logging.warning("Header dump unsuccessful.")

def generate_header_yaml(data_processor):
    #  Generates a list of headers
    logging.info("Compiling list of json headers...")
    headers = {}
    for flattened_json in os.listdir(TEMP_DIR):
        file = load_json(Path(TEMP_DIR) / flattened_json)
        for item in file:
            for header in item:
                if header not in headers:
                    headers[header] = True
    dump_headers_to_yaml(headers, data_processor.export_type)
    logging.info("Header list compiled successfully.")

def report_csv_rows_columns(csv_file):
    #  Reports a count of a csv file's rows and columns
    logging.info(f"Reporting {csv_file} column count...")
    try:
        with open(csv_file) as file:
            data = list(csv.reader(file))
            logging.info(f"{csv_file} opened successfully.")
            print(f"{csv_file} Row Count:", len(data))
            print(f"{csv_file} Column Count:", len(data[0]))
    except FileNotFoundError:
        logging.warning(f"{csv_file} not found. Skipping...")
    except PermissionError:
        logging.warning("Insufficient permissions. Skipping...")

def purge_temp():
    #  Deletes all files in the /temp/ directory
    logging.info(f"Purging {TEMP_DIR}...")
    for root, dirs, files in os.walk(TEMP_DIR):
        for file in files:
            os.remove(os.path.join(root, file))
    logging.info(f"{TEMP_DIR} purged successfully.")