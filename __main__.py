#!/usr/bin/env python3.12
#-*- coding: utf-8 -*- 

from util.vuln_export import *
from util.config import *
from util.asset_export import *

def main():
    setup_logger()
    setup_data()
    vuln_export()
    asset_export()
    sys.exit(0)

def vuln_export():
    vuln_export = VulnExport()
    vuln_export.request_vuln_export()
    vuln_export.request_vuln_export_status()
    vuln_export.download_all_vuln_chunks()
    return 0

def asset_export():
    asset_export = AssetExport()
    asset_export.request_asset_export()
    asset_export.request_asset_export_status()
    asset_export.request_asset_export_jobs() # Required due to asset export status metadata differing from vulnerability export metadata
    asset_export.download_all_asset_chunks()
    return 0

if __name__ == "__main__":
    main()
