import json
import pandas as pd
import csv
import yaml
from flatten_json import flatten

TEST_FILE = r"C:\Users\pam62425\OneDrive - Science and Technology Facilities Council\Documents\Projects\Graduate Rotation 1\pmt-dashboard\data\vulnerabilities\20240705_vuln\1720193639071_c29aaa39-a310-4dc3-823c-ce43a4a92e5f_1.json"
TEST_FILE2 = r"C:\Users\pam62425\OneDrive - Science and Technology Facilities Council\Documents\Projects\Graduate Rotation 1\pmt-dashboard\data\assets\20240705_asset\1720193694449_157f944e-abc0-4a2a-9a0e-cfe13ad71809_1.json"

def load_json(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

def flatten_json(json):
    flattened_data = []
    for item in json:
        if "output" in item:
            item.pop("output")
        flattened_data.append(flatten(item))
    return flattened_data

def write_json(flattened_data):
    with open("flattened_data.json", "w") as file:
        json.dump(flattened_data, file)

def write_heads_to_yaml(flattened_data):
    headers = {}
    with open("headers.yaml", "w") as file:
        for item in flattened_data:
            for header in item:
                if header not in headers:
                    headers[header] = True
        headers = dict(sorted(headers.items(), key=lambda x:x[1]))
        print(headers)
        yaml.dump(headers, file, default_flow_style=False)
        # json.dump(headers, file)    

def convert_json_to_csv(flattened_data):
    df = pd.DataFrame(flattened_data)
    df.to_csv("flattened_data.csv", encoding="utf-8", index=False)

def report_csv_columns(csv_file):
    with open(csv_file) as file:
        data = list(csv.reader(file))
    print("CSV Row Count:", len(data))
    print("CSV Column Count:", len(data[0]))

vuln = flatten_json(load_json(TEST_FILE))
write_heads_to_yaml(vuln)
# write_json(vuln)

asset = flatten_json(load_json(TEST_FILE2))
# write_heads_to_yaml(asset)
# write_json(asset)

# convert_json_to_csv(vuln)
# report_csv_columns(r"flattened_data.csv")