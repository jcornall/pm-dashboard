from src.config.transform_config import *
from pathlib import Path
import pandas as pd
import re
import json
import mariadb
import sys


class DatabaseLoader():

    def __init__(self):
        self.conn = self.connect_to_database

    def connect_to_database():
        try:
            conn = mariadb.connect(
                user="pmt-dashboard",
                password="@Scl7ps5&$",
                host="pam62425@host-172-16-105-249",
                port=22,
                database="tenable"
            )
            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB platform: {e}")
            sys.exit(1)
        
    def get_cursor(self):
        cursor = self.conn.cursor()

