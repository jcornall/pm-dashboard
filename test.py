# from util.extract.tenable_vuln_export import *
# from util.extract.tenable_asset_export import *
# from util.extract.config import *

# test_vuln_export = VulnExport()
# # test_vuln_export.request_vuln_export()
# test_vuln_export.uuid = "95b21172-94f8-4800-b55b-801d5b9f3414"
# test_vuln_export.request_vuln_export_status()
# test_vuln_export.download_all_vuln_chunks()

# {"status":"FINISHED","chunks_available":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]}
# json = {"exports":[{"uuid":"15a6510d-14df-485d-bb88-4371d8792a0d",
#              "status":"FINISHED",
#              "total_chunks":17,
#              "filters":"{}",
#              "finished_chunks":17,
#              "num_assets_per_chunk":500,
#              "created":1719485419313},
             
#              {"uuid":"e0d8ff65-e42f-4393-8838-c65b1b081658",
#               "status":"FINISHED",
#               "total_chunks":83,
#               "filters":"{}",
#               "finished_chunks":83,
#               "num_assets_per_chunk":100,
#               "created":1718698015386}]}

# from src.config.resource import *
# from src.config.constants import *

# from flatten_json import flatten
# import yaml
# import json

# def load_json(json_file):
#     #  Load a json data file
#     with open(json_file) as file:
#         data = json.load(file)
#     return data

# def flatten_json(json_file, headers):
#     #  Flatten the json data file's nested hierarchy
#     flattened_data = []
#     with open(headers, "r") as file:
#             config = yaml.safe_load(file)
#     for item in json_file:
#         flattened_item = flatten(item)
#         for header in list(flattened_item):
#             if (config[header] != True):
#                  flattened_item.pop(header)
#         flattened_data.append(flattened_item)
#     return flattened_data

# with open(VULN_HEADERS, "r") as file:
#     config = yaml.safe_load(file)
#     print(config["output"])
#     json_file = 
#     for item in load_json(file):
#         print(item)
            # if "output" in item:
            #     item.pop("output")
        #     flattened_data.append(flatten(item))
        # return flattened_data

# def write_json(flattened_data):
#         #  Write the flattened json data file to the /temp/ directory
#         with open("flattened_data.json", "w") as file:
#             json.dump(flattened_data, file)

# flattened_data = flatten_json(load_json(TEST_FILE), VULN_HEADERS)
# write_json(flattened_data)
