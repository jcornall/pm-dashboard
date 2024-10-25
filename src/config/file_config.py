#!/usr/bin/env python3.12
#-*- coding: utf-8 -*-
"""This module contains methods used to configure the extract functionality of the program, as well as setting up and maintaining the data file structure.
"""

from src.config.constants import *
from pathlib import Path
import logging
import os
import datetime as dt

def set_up_file_structure():
    """Sequence method calls to set up the data file structure."""
    set_up_dir(DATA_DIR)
    set_up_dir(VULN_DATA_DIR)
    set_up_subdir(VULN_EXPORT_DIR)
    set_up_dir(ASSET_DATA_DIR)
    set_up_subdir(ASSET_EXPORT_DIR)
    set_up_dir(COMPLIANCE_DATA_DIR)
    set_up_subdir(COMPLIANCE_EXPORT_DIR)
    set_up_dir(TEMP_DIR)
    set_up_dir(PROCESSED_DIR)
    return 0

def set_up_dir(dir_path):
    """Setup a directory using the supplied directory path."""
    logging.info(f"Checking if {dir_path} directory exists...")
    try:
        os.mkdir(dir_path)
        logging.warning(f"Directory does not exist, creating {dir_path} directory...")
        logging.info(f"{dir_path} directory created.")
    except FileExistsError as e:
        logging.info(f"Error: {e}.")

def set_up_subdir(dir_path):
    """Setup a subdirectory using the supplied directory path."""
    logging.info(f"Checking if {dir_path} subdirectory exists...")
    try:
        os.mkdir(dir_path)
        logging.warning(f"Subdirectory does not exist, creating {dir_path} directory...")
        logging.info(f"{dir_path} subdirectory created.")
    except FileExistsError as e:
        logging.info(f"Error: {e}.")

def purge_old_files(dir_path):
    """Purge a directory of all files in the supplied directory path older than the RETENTION_PERIOD constant."""
    logging.info(f"Retention Period: {RETENTION_PERIOD}...")
    logging.info(f"Purging old files...")
    count = 0
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            creation_datetime = dt.datetime.fromtimestamp((os.path.getctime(os.path.join(root, file))))
            current_datetime = dt.datetime.today()
            if creation_datetime < (current_datetime - dt.timedelta(days=RETENTION_PERIOD)):
                # logging.info(f"Deleting {file}...")
                try:
                    os.remove(os.path.join(root, file))
                    count += 1
                    # logging.info(f"{file} deleted.")
                except FileNotFoundError as e:
                    logging.warning(f"Error: {e}. Skipping...")
                except PermissionError as e:
                    logging.warning(f"Error: {e}. Skipping...")
    logging.info(f"{count} files purged successfully.")

def purge_empty_dirs(dir_path):
    """Purge all empty directories."""
    logging.info(f"Purging empty directories...")
    count = 0
    for root, dirs, files in os.walk(dir_path):
        for dir in dirs:
            if len(os.listdir(os.path.join(root, dir))) == 0:
                # logging.info(f"Deleting {dir}...")
                try:
                    os.removedirs(os.path.join(root, dir))
                    count += 1
                    # logging.info(f"{dir} deleted.")
                except FileNotFoundError as e:
                    logging.warning(f"Error: {e}. Skipping...")
                except PermissionError as e:
                    logging.warning(f"Error: {e}. Skipping...")
    logging.info(f"{count} directories purged successfully.")