#!/usr/bin/env python3.12
#-*- coding: utf-8 -*-
"""This module is used for testing.
"""

from src.util.extract.api_export import *
from src.util.extract.asset_export import *
from src.util.extract.vuln_export import *
from src.util.transform.data_processor import *
from src.util.load.database_loader import *
from src.config.transform_config import *
from src.config.constants import *
from src.config.extract_config import *
from src.config.logger_config import *


def export_vuln():
    """Sequence API calls to Tenable service and return downloaded vulnerability data."""
    vuln_export = VulnExport()
    vuln_export.post_vuln_export()
    vuln_export.get_vuln_export_status()
    vuln_export.download_all_vuln_chunks()
    return 0

def export_asset():
    """Sequence API calls to Tenable service and return downloaded asset data."""
    asset_export = AssetExport()
    asset_export.post_asset_export()
    asset_export.get_asset_export_status()
    asset_export.get_asset_export_jobs()  # Required due to asset export status metadata differing from vulnerability export metadata
    asset_export.download_all_asset_chunks()
    return 0

def export_compliance():
    """Sequence API calls to Tenable service and return downloaded compliance data."""
    compliance_export = ComplianceExport()
    compliance_export.post_compliance_export()
    compliance_export.get_compliance_export_status()
    compliance_export.get_compliance_export_jobs()  # Required due to asset export status metadata differing from vulnerability export metadata
    compliance_export.download_all_compliance_chunks()
    return 0

def process_data(file_path):
    """Sequence DataProcessor calls to DataProcessor."""
    data_processor = DataProcessor(file_path)
    data_processor.transform_data(data_processor.dir_path, data_processor.header_file, data_processor.export_type)
    # configure_data_processor(data_processor)
    return 0

def configure_data_processor(data_processor):
    """Configure the DataProcessor by generating new YAML files containing all JSON data headers."""
    generate_header_yaml(data_processor)

def load_data(data_type, sql_file_path):
    """Load the data into a MariaDB database."""
    database_loader = DatabaseLoader(data_type, CONN_PARAMS)
    # database_loader.drop_table(database_loader.cursor, "tenable", table)
    database_loader.create_table(database_loader.cursor, sql_file_path, "create_export_table.sql")
    database_loader.create_table(database_loader.cursor, sql_file_path, "create_timeseries_table.sql")
    database_loader.load_csv(database_loader.cursor, sql_file_path, "load_csv.sql")
    database_loader.insert_into_table(database_loader.cursor, sql_file_path, "insert_into_timeseries_table.sql")
    database_loader.delete_from_table(database_loader.cursor, sql_file_path, "delete_from_export_table.sql")
    database_loader.select_count(database_loader.cursor, sql_file_path, "select_count_export_table.sql")
    database_loader.select_count(database_loader.cursor, sql_file_path, "select_count_timeseries_table.sql")
    database_loader.conn.commit()
    database_loader.cursor.close()
    database_loader.close_connection()

# # Main
print(f"Current Working Directory: {Path.cwd()}")
set_up_logger()
logging.info("Logger setup successful.")
purge_old_files(DATA_DIR)
purge_old_files(LOGS_DIR)
logging.info("Old data purge successful...")
purge_empty_dirs(DATA_DIR)
purge_empty_dirs(LOGS_DIR)
logging.info("Empty data directory purge successful...")
logging.info("Data extraction successful.")
set_up_file_structure()
logging.info("File structure setup successful.")

# # Extract
# # logging.info("Starting data extraction...")
# # export_vuln()
# # logging.info("Vulnerability data extraction successful...")
# # export_asset()
# # logging.info("Asset data extraction successful...")
export_compliance()
logging.info("Compliance data extraction successful...")

# # Transform
# logging.info("Starting data transformation...")
# purge_dir(PROCESSED_DIR)
# process_data(VULN_EXPORT_DIR)
# process_data(ASSET_EXPORT_DIR)
# process_data(COMPLIANCE_EXPORT_DIR)
# logging.info("Data transformation successful.")

# # Load
# logging.info("Starting data loading...")
# load_data("vulnerabilities", TENABLE_SQL_DIR / "vulnerabilities")
# load_data("assets", TENABLE_SQL_DIR / "assets")
# load_data("compliance", TENABLE_SQL_DIR / "compliance")

# logging.info("Program execution successful, exiting program.")
# sys.exit(0)