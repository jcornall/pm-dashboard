from util.extract.config import *
import json
import pandas as pd
import csv
import yaml
from flatten_json import flatten

TEST_FILE = r"C:\Users\pam62425\OneDrive - Science and Technology Facilities Council\Documents\Projects\Graduate Rotation 1\pmt-dashboard\1720626296255_32f50088-cc41-46f7-883b-5317343562b7_1.json"
TEST_FILE2 = r"C:\Users\pam62425\OneDrive - Science and Technology Facilities Council\Documents\Projects\Graduate Rotation 1\pmt-dashboard\1720626360688_18ed6cd5-25b1-4cd7-b126-1a944713d116_1.json"

"""
def transform_data(file_path, output_file_name):
    purge_temp()
    for file in file_path:
        flattened_data = flatten_json(load_json(file))
        csv_file = TEMP_DIR / f"{self.created}_{self.uuid}_{chunk}.json"
        convert_json_to_csv(csv_file, re.split(".", file)[0])
    merge_csv_files(output_file_name)
    return 0
"""

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

# def write_json(flattened_data):
#     #  Write the flattened json data file to the /temp/ directory
#     with open("flattened_data.json", "w") as file:
#         json.dump(flattened_data, file)

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

def convert_json_to_csv(flattened_data, file_name):
    df = pd.DataFrame(flattened_data)
    df.to_csv(TEMP_DIR / f"{file_name}.csv", encoding="utf-8", index=False)

def report_csv_columns(csv_file):
    with open(csv_file) as file:
        data = list(csv.reader(file))
    print(f"{csv_file} Row Count:", len(data))
    print(f"{csv_file} Column Count:", len(data[0]))

"""def merge_csv_files():
    for file in TEMP_DIR:
        
"""

def purge_temp():
    for root, dirs, files in os.walk(TEMP_DIR):
        for file in files:
            os.remove(os.path.join(root, file))

vuln = flatten_json(load_json(TEST_FILE))
write_headers_to_yaml(vuln)

asset = flatten_json(load_json(TEST_FILE2))
write_headers_to_yaml(asset)

# convert_json_to_csv(vuln)
# report_csv_columns(r"flattened_data.csv")