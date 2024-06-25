from vuln_export import *
# from util.asset_export import *

test_vuln_export = VulnExport()
# test_uuid = test_vuln_export.request_vuln_export()
test_uuid = "fa957f6e-6376-45d1-b106-e0f0d969e78f"
test_vuln_export.request_vuln_export_status(test_uuid)
test_vuln_export.download_all_vuln_chunks()