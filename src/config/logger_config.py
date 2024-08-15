#!/usr/bin/env python3.12
#-*- coding: utf-8 -*-
"""This module contains methods to set up and configure the Python logging functionality.
"""

from src.config.constants import *
import logging
import os

def set_up_logger():
    """Set up /log/ directory for log files."""
    try:
        os.mkdir(LOGS_DIR)
    except FileExistsError:
        pass
    try:
        os.mkdir(EXPORT_LOG_DIR)
    except FileExistsError:
        pass
    EXPORT_LOG_FILE = EXPORT_LOG_DIR / f"{FORMATTED_DATE}_{FORMATTED_TIME}.log"
    logging.basicConfig(level=logging.INFO, filename=EXPORT_LOG_FILE, filemode="w", format="%(asctime)s:%(name)s:%(module)s:%(levelname)s - %(message)s")
    logging.info(f"Initiating log file {FORMATTED_TIME}.log.")
    logging.info(f"Application started in {os.getcwd()}.")
    return 0