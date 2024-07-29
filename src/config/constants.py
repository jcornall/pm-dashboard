from pathlib import Path
import datetime as dt


#  Date & Time
CURRENT = dt.datetime.now()
FORMATTED_DATE = CURRENT.strftime("%Y%m%d")
FORMATTED_TIME = CURRENT.strftime("%H%M%S")

#  Filepaths
LOGS_DIR = Path(r"logs")
EXPORT_LOG_DIR = LOGS_DIR / FORMATTED_DATE

DATA_DIR = Path(r"data")
TEMP_DIR = DATA_DIR / "temp"
PROCESSED_DIR = DATA_DIR / "processed"
VULN_DATA_DIR = DATA_DIR / "vulnerabilities"
VULN_EXPORT_DIR = VULN_DATA_DIR / f"{FORMATTED_DATE}_vuln"
ASSET_DATA_DIR = DATA_DIR / "assets"
ASSET_EXPORT_DIR = ASSET_DATA_DIR / f"{FORMATTED_DATE}_asset"
RESOURCE_DIR = Path(r"src\config\resource")

#  Data Configuration
RETENTION_PERIOD = 3

#  Testing
# TEST_FILE = r"data\1720626296255_32f50088-cc41-46f7-883b-5317343562b7_1.json"
# TEST_FILE2 = r"data\1720626360688_18ed6cd5-25b1-4cd7-b126-1a944713d116_1.json"
