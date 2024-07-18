# #!/usr/bin/env python3.12
# #-*- coding: utf-8 -*- 

# from src.util.extract.api_export import *
# from src.util.extract.asset_export import *
# from src.util.extract.vuln_export import *
# from src.util.transform.data_processor import *
# from src.config.transform_config import *
# from src.config.constants import *
# from src.config.extract_config import *
# from src.config.logger_config import *


# def export_vuln():
#     #  Sequence API calls to Tenable service in order to download vulnerability data
#     vuln_export = VulnExport()
#     vuln_export.request_vuln_export()
#     vuln_export.request_vuln_export_status()
#     vuln_export.download_all_vuln_chunks()
#     return 0

# def export_asset():
#     #  Sequence API calls to Tenable service in order to download asset data
#     asset_export = AssetExport()
#     asset_export.request_asset_export()
#     asset_export.request_asset_export_status()
#     asset_export.request_asset_export_jobs()  #  Required due to asset export status metadata differing from vulnerability export metadata
#     asset_export.download_all_asset_chunks()
#     return 0

# def process_data(file_path):
#     data_processor = DataProcessor(file_path)
#     data_processor.transform_data()
#     # configure_data_processor(data_processor)
#     # data_processor.merge_data()
#     return 0

# def configure_data_processor(data_processor):
#     generate_header_yaml(data_processor)

# # # Main
# print(f"Current Working Directory: {Path.cwd()}")
# setup_logger()
# logging.info("Logger setup successful.")
# setup_file_structure()
# logging.info("File structure setup successful.")
# # configure_data_processor()

# # # #  Extract
# # logging.info("Extracting data...")
# # export_vuln()
# # logging.info("Vulnerability data extraction successful...")
# # export_asset()
# # logging.info("Asset data extraction successful...")
# # purge_old_files(DATA_DIR)
# # purge_old_files(LOGS_DIR)
# # logging.info("Old data purge successful...")
# # purge_empty_dirs(DATA_DIR)
# # purge_empty_dirs(LOGS_DIR)
# # logging.info("Empty data directory purge successful...")
# # logging.info("Extraction successful.")

# #  Transform
# # logging.info("Transforming data...")
# # process_data(r"C:\Users\pam62425\OneDrive - Science and Technology Facilities Council\Documents\Projects\Graduate Rotation 1\pmt-dashboard\data\vulnerabilities\20240710_vuln")
# # logging.info("Transformation successful.")
