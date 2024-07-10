import logging
import logging.handlers as handlers
from pathlib import Path
from dotenv import load_dotenv
import os
import datetime

ENV_PATH = Path(".") / ".env"
load_dotenv(dotenv_path=ENV_PATH)

CURRENT = datetime.datetime.now()
FORMATTED_DATE = CURRENT.strftime("%Y%m%d")
FORMATTED_TIME = CURRENT.strftime("%H%M%S")

LOGS_DIR = Path.cwd() / "logs"
EXPORT_LOG_DIR = LOGS_DIR / FORMATTED_DATE
DATA_DIR = Path.cwd() / "data"
VULN_DATA_DIR = DATA_DIR / "vulnerabilities"
VULN_EXPORT_DIR = VULN_DATA_DIR / f"{FORMATTED_DATE}_vuln"
ASSET_DATA_DIR = DATA_DIR / "assets"
ASSET_EXPORT_DIR = ASSET_DATA_DIR / f"{FORMATTED_DATE}_asset"

DATA_EXPIRATION = 3

def setup_logger():
    # Setup /log/ directory
    try:
        os.mkdir(LOGS_DIR)
    except FileExistsError:
        pass

    # Setup timestamped /log/ subdirectory
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
    # Setup /data/ directory
    try:
        os.mkdir(DATA_DIR)
    except FileExistsError:
        pass
    # Setup /data/vulnerabilities/ directory
    setup_directory(VULN_DATA_DIR)
    # Setup timestamped /data/vulnerabilities/ subdirectory
    setup_subdirectory(VULN_EXPORT_DIR)
    # Setup /data/assets/ directory
    setup_directory(ASSET_DATA_DIR)
    # Setup timestamped /data/assets/ subdirectory
    setup_subdirectory(ASSET_EXPORT_DIR)
    return 0

def setup_directory(file_path):
    # Setup /file_path/ directory
    logging.info(f"Checking if {file_path} directory exists...")
    try:
        os.mkdir(file_path)
        logging.warning(f"Directory does not exist, creating {file_path} directory...")
        logging.info(f"{file_path} directory created.")
    except FileExistsError:
        logging.info(f"{file_path} directory exists.")

def setup_subdirectory(file_path):
    # Setup /file_path/ subdirectory
    logging.info(f"Checking if {file_path} subdirectory exists...")
    try:
        os.mkdir(file_path)
        logging.warning(f"Subdirectory does not exist, creating {file_path} directory...")
        logging.info(f"{file_path} subdirectory created.")
    except FileExistsError:
        logging.info(f"{file_path} subdirectory exists.") 

def cull_old_data():
    # Cull aged data older than DATA_EXPIRATION days
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            creation_datetime = datetime.datetime.fromtimestamp((os.path.getctime(os.path.join(root, file))))
            current_datetime = datetime.datetime.today()
            if creation_datetime > (current_datetime - datetime.timedelta(days=DATA_EXPIRATION)):
                os.remove(os.path.join(root, file))

def cull_empty_directories():
    # Cull empty directories
    for root, dirs, files in os.walk(DATA_DIR):
        for dir in dirs:
            if len(os.listdir(os.path.join(root, dir))) == 0:
                print("is empty")
                os.removedirs(os.path.join(root, dir))