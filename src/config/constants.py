#!/usr/bin/env python3.12
#-*- coding: utf-8 -*-
"""This module contains all constants relevant to the various modules of this program.
"""

from pathlib import Path
from dotenv import load_dotenv
import datetime as dt
import time
import os

# Date & Time
CURRENT = dt.datetime.now()
FORMATTED_DATE = CURRENT.strftime("%Y%m%d")
FORMATTED_TIME = CURRENT.strftime("%H%M%S")

# Filepaths
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
COMPLIANCE_DATA_DIR = DATA_DIR / "compliance"
COMPLIANCE_EXPORT_DIR = COMPLIANCE_DATA_DIR / f"{FORMATTED_DATE}_compliance"
RESOURCE_DIR = Path(r"src") / "config" / "resource"
TENABLE_SQL_DIR = RESOURCE_DIR / "sql" / "tenable"


# Keys
load_dotenv(dotenv_path=ENV_PATH)
TENABLE_ACCESS_KEY = os.getenv("TENABLE_ACCESS_KEY")
TENABLE_SECRET_KEY = os.getenv("TENABLE_SECRET_KEY")
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_PWD = os.getenv("MARIADB_PWD")
MARIADB_HOST = os.getenv("MARIADB_HOST")
MARIADB_PORT = int(os.getenv("MARIADB_PORT"))
MARIADB_DB = os.getenv("MARIADB_DB")

# MariaDB Connection Parameters
CONN_PARAMS = {
    "user":MARIADB_USER,
    "password":MARIADB_PWD,
    "host":MARIADB_HOST,
    "port":MARIADB_PORT,
    "database":MARIADB_DB
}

# Data Configuration
RETENTION_PERIOD = 3 
VULNEXPORT_FILTER_SINCE = int(time.mktime((dt.datetime.now() - dt.timedelta(days=365)).timetuple()))