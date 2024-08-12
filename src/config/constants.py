from pathlib import Path
import datetime as dt
import time
import os 


#  Date & Time
CURRENT = dt.datetime.now()
FORMATTED_DATE = CURRENT.strftime("%Y%m%d")
FORMATTED_TIME = CURRENT.strftime("%H%M%S")

#  Keys
TENABLE_ACCESS_KEY = os.getenv("TENABLE_ACCESS_KEY")
TENABLE_SECRET_KEY = os.getenv("TENABLE_SECRET_KEY")
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_PWD = os.getenv("MARIADB_PWD")
MARIADB_HOST = os.getenv("MARIADB_HOST")
MARIADB_PORT = os.getenv("MARIADB_PORT")
MARIADB_DB = os.getenv("MARIADB_DB")

#  Filepaths
ENV_PATH = Path(".") / ".env"
LOGS_DIR = Path(r"logs")
EXPORT_LOG_DIR = LOGS_DIR / FORMATTED_DATE
DATA_DIR = Path(r"data")
TEMP_DIR = DATA_DIR / "temp"
PROCESSED_DIR = DATA_DIR / "processed"
VULN_DATA_DIR = DATA_DIR / "vulnerabilities"
VULN_EXPORT_DIR = VULN_DATA_DIR / f"{FORMATTED_DATE}_vuln"
ASSET_DATA_DIR = DATA_DIR / "assets"
ASSET_EXPORT_DIR = ASSET_DATA_DIR / f"{FORMATTED_DATE}_asset"
RESOURCE_DIR = Path(r"src") / "config" / "resource"
SQL_DIR = RESOURCE_DIR / "sql"

#  Data Configuration
RETENTION_PERIOD = 3 
VULNEXPORT_FILTER_SINCE = int(time.mktime((dt.datetime.now() - dt.timedelta(days=365)).timetuple()))

#  Testing
# TEST_FILE = r"data\1720626296255_32f50088-cc41-46f7-883b-5317343562b7_1.json"
# TEST_FILE2 = r"data\1720626360688_18ed6cd5-25b1-4cd7-b126-1a944713d116_1.json"

#  MariaDB Connection Parameters
CONN_PARAMS = {
    "user":MARIADB_USER,
    "password":MARIADB_PWD,
    "host":MARIADB_HOST,
    "port":MARIADB_PORT,
    "database":MARIADB_DB
}