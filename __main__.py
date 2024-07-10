#!/usr/bin/env python3.12
#-*- coding: utf-8 -*- 

from util.extract.tenable_vuln_export import *
from util.extract.tenable_asset_export import *
from util.extract.config import *

def main():
    setup_logger()
    setup_data()
    vuln_export()
    asset_export()
    cull_old_data()
    cull_empty_directories()
    sys.exit(0)

def vuln_export():
    # Sequence API calls to Tenable service in order to download vulnerability data
    vuln_export = TenableVulnExport()
    vuln_export.request_vuln_export()
    vuln_export.request_vuln_export_status()
    vuln_export.download_all_vuln_chunks()
    return 0

def asset_export():
    # Sequence API calls to Tenable service in order to download asset data
    asset_export = TenableAssetExport()
    asset_export.request_asset_export()
    asset_export.request_asset_export_status()
    asset_export.request_asset_export_jobs()  # Required due to asset export status metadata differing from vulnerability export metadata
    asset_export.download_all_asset_chunks()
    return 0

if __name__ == "__main__":
    main()