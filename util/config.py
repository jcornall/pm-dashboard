#!/usr/bin/env python3.12
#-*- coding: utf-8 -*- 

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
VULN_DATA_DIR = DATA_DIR / "vulnerabilities"
VULN_EXPORT_DIR = VULN_DATA_DIR / f"{FORMATTED_DATE}_vuln"
ASSET_DATA_DIR = DATA_DIR / "assets"
ASSET_EXPORT_DIR = ASSET_DATA_DIR / f"{FORMATTED_DATE}_asset"

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
    logging.info(f"Checking if {VULN_DATA_DIR} directory exists...")
    try:
        os.mkdir(VULN_DATA_DIR)
        logging.warning(f"Directory does not exist, creating {VULN_DATA_DIR} directory...")
        logging.info(f"{VULN_DATA_DIR} directory created.")
    except FileExistsError:
        logging.info(f"{VULN_DATA_DIR} directory exists.") 

    # Setup timestamped /data/vulnerabilities/ subdirectory
    logging.info(f"Checking if {VULN_EXPORT_DIR} exists...")
    try:
        os.mkdir(VULN_EXPORT_DIR)
        logging.warning(f"Directory does not exist, creating {VULN_EXPORT_DIR} directory...")
        logging.info(f"{VULN_EXPORT_DIR} directory created.")
    except FileExistsError:
        logging.info(f"{VULN_EXPORT_DIR} directory exists.") 

        # Setup /data/assets/ directory
    logging.info(f"Checking if {ASSET_DATA_DIR} directory exists...")
    try:
        os.mkdir(ASSET_DATA_DIR)
        logging.warning(f"Directory does not exist, creating {ASSET_DATA_DIR} directory...")
        logging.info(f"{ASSET_DATA_DIR} directory created.")
    except FileExistsError:
        logging.info(f"{ASSET_DATA_DIR} directory exists.") 

    # Setup timestamped /data/assets/ subdirectory
    logging.info(f"Checking if {ASSET_EXPORT_DIR} exists...")
    try:
        os.mkdir(ASSET_EXPORT_DIR)
        logging.warning(f"Directory does not exist, creating {ASSET_EXPORT_DIR} directory...")
        logging.info(f"{ASSET_EXPORT_DIR} directory created.")
    except FileExistsError:
        logging.info(f"{ASSET_EXPORT_DIR} directory exists.") 

    return 0