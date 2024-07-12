from src.config.transform_config import *
from src.util.extract.api_export import APIExport
from pathlib import Path
import pandas as pd
import requests as re
import json


class DataProcessor():

    def __init__(self): 
        #  Instantiate DataProcessor object
        pass

    def set_values(self, file_path):
        self.dir_path = file_path
        self.data_type = re.split("_", file_path)[1]

    def transform_data(self):
        purge_temp()
        for file in self.dir_path:
            flattened_data = self.flatten_json(self.load_json(file))
            self.convert_json_to_csv(flattened_data, re.split(".", file)[0])
        self.merge_csv_files()
        return 0

    def load_json(self, json_file):
        #  Load a json data file
        with open(json_file) as file:
            data = json.load(file)
        return data
    
    def flatten_json(self, json_file, headers):
        #  Flatten the json data file's nested hierarchy
        flattened_data = []
        with open(headers, "r") as file:
                config = yaml.safe_load(file)
        for item in json_file:
            flattened_item = flatten(item)
            #  Checks headers against yml configuration file
            for header in list(flattened_item):
                if (config[header] != True):
                    flattened_item.pop(header)
            flattened_data.append(flattened_item)
        return flattened_data
    
    # def write_json(self, flattened_data):
    #     #  Write the flattened json data file to the /temp/ directory
    #     with open("flattened_data.json", "w") as file:
    #         json.dump(flattened_data, file)

    def convert_json_to_csv(self, flattened_data, file_name):
        df = pd.DataFrame(flattened_data)
        df.to_csv(TEMP_DIR / f"{file_name}.csv", encoding="utf-8", index=False)

    """
    def merge_data():
        for file in TEMP_DIR:
    """