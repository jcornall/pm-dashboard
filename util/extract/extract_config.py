import logging
# import logging.handlers as handlers
from pathlib import Path
from dotenv import load_dotenv
import os
import datetime as dt

ENV_PATH = Path(".") / ".env"
load_dotenv(dotenv_path=ENV_PATH)

CURRENT = dt.datetime.now()
FORMATTED_DATE = CURRENT.strftime("%Y%m%d")
FORMATTED_TIME = CURRENT.strftime("%H%M%S")

LOGS_DIR = Path.cwd() / "logs"
EXPORT_LOG_DIR = LOGS_DIR / FORMATTED_DATE
DATA_DIR = Path.cwd() / "data"
TEMP_DIR = DATA_DIR / "temp"
PROCESSED_DIR = DATA_DIR / "processed"
VULN_DATA_DIR = DATA_DIR / "vulnerabilities"
VULN_EXPORT_DIR = VULN_DATA_DIR / f"{FORMATTED_DATE}_vuln"
ASSET_DATA_DIR = DATA_DIR / "assets"
ASSET_EXPORT_DIR = ASSET_DATA_DIR / f"{FORMATTED_DATE}_asset"

RETENTION_PERIOD = 3

def setup_logger():
    #  Setup /log/ directory
    try:
        os.mkdir(LOGS_DIR)
    except FileExistsError:
        pass
    #  Setup timestamped /log/ subdirectory
    try:
        os.mkdir(EXPORT_LOG_DIR)
    except FileExistsError:
        pass
    EXPORT_LOG_FILE = EXPORT_LOG_DIR / f"{FORMATTED_DATE}_{FORMATTED_TIME}.log"
    logging.basicConfig(level=logging.INFO, filename=EXPORT_LOG_FILE, filemode="w", format="%(asctime)s:%(name)s:%(module)s:%(levelname)s - %(message)s")
    logging.info(f"Initiating log file {FORMATTED_TIME}.log.")
    logging.info(f"Application started in {os.getcwd()}.")
    return 0

def setup_data():
    #  Setup /data/ directory
    logging.info(f"Checking if {DATA_DIR} directory exists...")
    try:
        os.mkdir(DATA_DIR)
        logging.warning(f"Directory does not exist, creating {DATA_DIR} directory...")
        logging.info(f"{DATA_DIR} directory created.")
    except FileExistsError:
        logging.info(f"{DATA_DIR} directory exists.")
    #  Setup /data/vulnerabilities/ directory
    setup_dir(VULN_DATA_DIR)
    #  Setup timestamped /data/vulnerabilities/ subdirectory
    setup_subdir(VULN_EXPORT_DIR)
    #  Setup /data/assets/ directory
    setup_dir(ASSET_DATA_DIR)
    #  Setup timestamped /data/assets/ subdirectory
    setup_subdir(ASSET_EXPORT_DIR)
    #  Setup /temp/ directory
    try:
        os.mkdir(TEMP_DIR)
    except FileExistsError:
        pass
    return 0

def setup_dir(file_path):
    #  Setup /file_path/ directory
    logging.info(f"Checking if {file_path} directory exists...")
    try:
        os.mkdir(file_path)
        logging.warning(f"Directory does not exist, creating {file_path} directory...")
        logging.info(f"{file_path} directory created.")
    except FileExistsError:
        logging.info(f"{file_path} directory exists.")

def setup_subdir(file_path):
    #  Setup /file_path/ subdirectory
    logging.info(f"Checking if {file_path} subdirectory exists...")
    try:
        os.mkdir(file_path)
        logging.warning(f"Subdirectory does not exist, creating {file_path} directory...")
        logging.info(f"{file_path} subdirectory created.")
    except FileExistsError:
        logging.info(f"{file_path} subdirectory exists.") 

def purge_old_files(file_path):
    #  Cull aged data older than DATA_EXPIRATION days
    logging.info(f"Purging old files...")
    for root, dirs, files in os.walk(file_path):
        for file in files:
            creation_datetime = dt.datetime.fromtimestamp((os.path.getctime(os.path.join(root, file))))
            current_datetime = dt.datetime.today()
            if creation_datetime < (current_datetime - dt.timedelta(days=RETENTION_PERIOD)):
                logging.info(f"Deleting {file}...")
                try:
                    os.remove(os.path.join(root, file))
                    logging.info(f"{file} deleted.")
                except FileNotFoundError:
                    logging.warning(f"{file} not found. Skipping...")
                except PermissionError:
                    logging.warning(f"Insufficient permissions. Skipping...")
    logging.info(f"Old files purged successfully.")

def purge_empty_dirs(file_path):
    #  Cull empty directories
    logging.info(f"Purging empty directories...")
    for root, dirs, files in os.walk(file_path):
        for dir in dirs:
            if len(os.listdir(os.path.join(root, dir))) == 0:
                logging.info(f"Deleting {dir}...")
                try:
                    os.removedirs(os.path.join(root, dir))
                    logging.info(f"{dir} deleted.")
                except FileNotFoundError:
                    logging.warning(f"{dir} not found. Skipping...")
                except PermissionError:
                    logging.warning(f"Insufficient permissions. Skipping...")
    logging.info(f"Empty directories purged successfully.")