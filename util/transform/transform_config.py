from util.extract.extract_config import *
import json
import csv
import yaml
import os
from flatten_json import flatten

TEST_FILE = r"C:\Users\pam62425\OneDrive - Science and Technology Facilities Council\Documents\Projects\Graduate Rotation 1\pmt-dashboard\1720626296255_32f50088-cc41-46f7-883b-5317343562b7_1.json"
TEST_FILE2 = r"C:\Users\pam62425\OneDrive - Science and Technology Facilities Council\Documents\Projects\Graduate Rotation 1\pmt-dashboard\1720626360688_18ed6cd5-25b1-4cd7-b126-1a944713d116_1.json"

def load_json(json_file):
    #  Load a json data file
    with open(json_file) as file:
        data = json.load(file)
    return data

def flatten_json(json_file):
    #  Flatten the json data file's nested hierarchy
    flattened_data = []
    for item in json_file:
        # if "output" in item:
        #     item.pop("output")
        flattened_data.append(flatten(item))
    return flattened_data

def write_headers_to_yaml(flattened_data):
    #  Write the flattened json data file's headers to a YAML file
    headers = {}
    with open("headers.yaml", "w") as file:
        for item in flattened_data:
            for header in item:
                if header not in headers:
                    headers[header] = True
        headers = dict(sorted(headers.items(), key=lambda x:x[1]))
        print(headers)
        yaml.dump(headers, file, default_flow_style=False) 

def report_csv_columns(csv_file):
    with open(csv_file) as file:
        data = list(csv.reader(file))
    print(f"{csv_file} Row Count:", len(data))
    print(f"{csv_file} Column Count:", len(data[0]))

def purge_temp():
    for root, dirs, files in os.walk(TEMP_DIR):
        for file in files:
            os.remove(os.path.join(root, file))