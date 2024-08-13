from src.config.constants import *
# import logging.handlers as handlers
from pathlib import Path
import logging
import os
import datetime as dt


def setup_file_structure():
    setup_dir(DATA_DIR)
    setup_dir(VULN_DATA_DIR)
    setup_subdir(VULN_EXPORT_DIR)
    setup_dir(ASSET_DATA_DIR)
    setup_subdir(ASSET_EXPORT_DIR)
    setup_dir(TEMP_DIR)
    setup_dir(PROCESSED_DIR)
    return 0

def setup_dir(file_path):
    #  Setup /file_path/ directory
    logging.info(f"Checking if {file_path} directory exists...")
    try:
        os.mkdir(file_path)
        logging.warning(f"Directory does not exist, creating {file_path} directory...")
        logging.info(f"{file_path} directory created.")
    except FileExistsError as e:
        logging.info(f"Error: {e}.")

def setup_subdir(file_path):
    #  Setup /file_path/ subdirectory
    logging.info(f"Checking if {file_path} subdirectory exists...")
    try:
        os.mkdir(file_path)
        logging.warning(f"Subdirectory does not exist, creating {file_path} directory...")
        logging.info(f"{file_path} subdirectory created.")
    except FileExistsError as e:
        logging.info(f"Error: {e}.")

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
                except FileNotFoundError as e:
                    logging.warning(f"Error: {e}. Skipping...")
                except PermissionError as e:
                    logging.warning(f"Error: {e}. Skipping...")
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
                except FileNotFoundError as e:
                    logging.warning(f"Error: {e}. Skipping...")
                except PermissionError as e:
                    logging.warning(f"Error: {e}. Skipping...")
    logging.info(f"Empty directories purged successfully.")