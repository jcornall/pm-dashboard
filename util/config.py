import logging
import logging.handlers as handlers
from pathlib import Path
import os
import datetime

CURRENT = datetime.datetime.now()
FORMATTED_DATE = CURRENT.strftime("%Y%m%d")
FORMATTED_TIME = CURRENT.strftime("%H%M%S")

LOGS_DIR = Path.cwd() / "logs"
EXPORT_LOG_DIR = LOGS_DIR / FORMATTED_DATE
DATA_DIR = Path.cwd() / "data"
VULN_EXPORT_DATA_DIR = DATA_DIR / f"{FORMATTED_DATE}_vuln"
ASSET_EXPORT_DATA_DIR = DATA_DIR / f"{FORMATTED_DATE}_asset"

def setup_logger():
    # Setup /log/ directory
    try:
        os.mkdir(LOGS_DIR)
    except FileExistsError:
        pass
    # Setup export-specific /log/ subdirectory
    try:
        os.mkdir(EXPORT_LOG_DIR)
    except FileExistsError:
        pass
    EXPORT_LOG_FILE = EXPORT_LOG_DIR / f"{FORMATTED_DATE}_{FORMATTED_TIME}.log"
    logging.basicConfig(level=logging.INFO, filename=EXPORT_LOG_FILE, filemode="w", format="%(asctime)s:%(name)s:%(module)s:%(levelname)s - %(message)s")
    logging.info(f"Initiating log file {FORMATTED_TIME}.log.")
    logging.info(f"Application started in {os.getcwd()}.")
    print(EXPORT_LOG_FILE)

def setup_data():
    # Setup /data/ directory
    logging.info(f"Checking if {DATA_DIR} directory exists...")
    try:
        os.mkdir(DATA_DIR)
        logging.warning(f"Directory does not exist, creating {DATA_DIR} directory...")
        logging.info(f"{DATA_DIR} directory created.")
    except FileExistsError:
        logging.info(f"{DATA_DIR} directory exists.") 
    # Setup export-specific /data/ subdirectory
    logging.info(f"Checking if {VULN_EXPORT_DATA_DIR} exists...")
    try:
        os.mkdir(VULN_EXPORT_DATA_DIR)
        logging.warning(f"Directory does not exist, creating {VULN_EXPORT_DATA_DIR} directory...")
        logging.info(f"{VULN_EXPORT_DATA_DIR} directory created.")
    except FileExistsError:
        logging.info(f"{VULN_EXPORT_DATA_DIR} directory exists.") 