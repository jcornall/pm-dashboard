from util.vuln_export import *
from util.config import *
# from util.asset_export import *

def main():
    setup_logger()
    setup_data()
    vuln_export = VulnExport()
    # vuln_export.request_vuln_export()
    vuln_export.uuid = "95b21172-94f8-4800-b55b-801d5b9f3414"
    vuln_export.request_vuln_export_status()
    vuln_export.download_all_vuln_chunks()

if __name__ == "__main__":
    main()