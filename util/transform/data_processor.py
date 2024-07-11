from util.transform.transform_config import *
from util.extract.api_export import APIExport
import pandas as pd
import json

class DataProcessor():

    def __init__(self): 
        #  Instantiate DataProcessor object
        pass

    def set_values(file_path):
        self.dir_path = file_path
        self.data_type = null

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
    
    def write_json(flattened_data):
        #  Write the flattened json data file to the /temp/ directory
        with open("flattened_data.json", "w") as file:
            json.dump(flattened_data, file)

    def convert_json_to_csv(flattened_data, file_name):
        df = pd.DataFrame(flattened_data)
        df.to_csv(TEMP_DIR / f"{file_name}.csv", encoding="utf-8", index=False)

    """
    def merge_csv_files():
        for file in TEMP_DIR:
    """