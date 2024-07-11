#!/usr/bin/env python3.12
#-*- coding: utf-8 -*- 

from util.extract.api_export import *
from util.extract.asset_export import *
from util.extract.extract_config import *
from util.extract.vuln_export import *
from util.transform.data_processor import *
from util.transform.transform_config import *

def main():
    setup_logger()
    setup_data()
    # configure_data_processor()

    # #  Extract
    vuln_export()
    asset_export()
    purge_old_files(DATA_DIR)
    purge_empty_dirs(DATA_DIR)
    purge_old_files(LOGS_DIR)
    purge_empty_dirs(LOGS_DIR)

    #  Transform
    # transform_data(, DATA_DIR / "processed")
    # transform_data()

    sys.exit(0)

def vuln_export():
    #  Sequence API calls to Tenable service in order to download vulnerability data
    vuln_export = VulnExport()
    vuln_export.request_vuln_export()
    vuln_export.request_vuln_export_status()
    vuln_export.download_all_vuln_chunks()
    return 0

def asset_export():
    #  Sequence API calls to Tenable service in order to download asset data
    asset_export = AssetExport()
    asset_export.request_asset_export()
    asset_export.request_asset_export_status()
    asset_export.request_asset_export_jobs()  #  Required due to asset export status metadata differing from vulnerability export metadata
    asset_export.download_all_asset_chunks()
    return 0

def transform_data():
    pass

def configure_data_processor():
    pass
    # vuln = flatten_json(load_json(TEST_FILE))
    # write_headers_to_yaml(vuln)

    # asset = flatten_json(load_json(TEST_FILE2))
    # write_headers_to_yaml(asset)

    # convert_json_to_csv(vuln)
    # report_csv_columns(r"flattened_data.csv")

if __name__ == "__main__":
    main()
