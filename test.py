#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""This module is used for testing .
"""

from src.util.extract.api_export import *
from src.util.transform.data_processor import *
from src.util.load.database_loader import *
from src.config.transform_config import *
from src.config.constants import *
from src.config.extract_config import *
from src.config.logger_config import *


def export_vuln():
    #  Sequence API calls to Tenable service in order to download vulnerability data
    pass


def export_asset():
    pass


def process_data(file_path):
    data_processor = DataProcessor(file_path)
    data_processor.transform_data(
        data_processor.dir_path, data_processor.header_file, data_processor.export_type
    )
    # configure_data_processor(data_processor)
    # data_processor.merge_data()
    return 0


def configure_data_processor(data_processor):
    generate_header_yaml(data_processor)


def load_data(table, create_statement, load_statement):
    database_loader = DatabaseLoader(table, CONN_PARAMS)
    database_loader.drop_table(database_loader.cursor, "tenable", table)
    database_loader.create_table(database_loader.cursor, create_statement)
    database_loader.load_csv(database_loader.cursor, load_statement)
    database_loader.conn.commit()
    database_loader.cursor.close()
    database_loader.close_connection()


# # Main
print(f"Current Working Directory: {Path.cwd()}")
set_up_logger()
logging.info("Logger setup successful.")
set_up_file_structure()
logging.info("File structure setup successful.")
# configure_data_processor()

# # #  Extract
# logging.info("Starting data extraction...")
# export_vuln()
# logging.info("Vulnerability data extraction successful...")
# export_asset()
# logging.info("Asset data extraction successful...")
# purge_old_files(DATA_DIR)
# purge_old_files(LOGS_DIR)
# logging.info("Old data purge successful...")
# purge_empty_dirs(DATA_DIR)
# purge_empty_dirs(LOGS_DIR)
# logging.info("Empty data directory purge successful...")
# logging.info("Data extraction successful.")

# # #  Transform
# logging.info("Starting data transformation...")
# purge_dir(PROCESSED_DIR)
# process_data(VULN_EXPORT_DIR)
# process_data(ASSET_EXPORT_DIR)
# logging.info("Data transformation successful.")

# # Load
logging.info("Starting data loading...")
load_data("vulnerabilities", "create_vuln_table.txt", "load_vuln_csv.txt")
# load_data("assets", "create_asset_table.txt", "load_asset_csv.txt")
