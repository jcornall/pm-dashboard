from src.config.transform_config import *
from src.config.constants import *
from pathlib import Path
import pandas as pd
import re
import json
import mariadb
import sys


class DatabaseLoader():

    def __init__(self, table, connection_parameters):
        self.conn = self.connect_to_database(connection_parameters)
        self.table = table
        self.cursor = self.set_cursor(self.conn)

    def connect_to_database(self, connection_parameters):
        logging.info(f"Connecting to {connection_parameters["host"]} as {connection_parameters["user"]}...")
        try:
            conn = mariadb.connect(**connection_parameters)
            logging.info(f"Successfully connected to {connection_parameters["host"]}.")
            return conn
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")
            sys.exit(1)

    def set_cursor(self, conn):
        cursor = conn.cursor()
        return cursor

    def drop_table(self, cursor, database, table):
        logging.info(f"Dropping existing MariaDB table {table} if it exists...")
        use_statement = f"USE {database}"
        drop_statement = f"DROP TABLE IF EXISTS {table}"
        try:
            cursor.execute(
                use_statement
            )
            cursor.execute(
                drop_statement
            )
            logging.info(f"MariaDB table {table} dropped.")
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")

    def create_table(self, cursor, sql_file):
        logging.info("Creating new MariaDB table...")
        file_path = SQL_DIR / sql_file
        try:
            with open(file_path, "r") as file:
                statement = file.read()
                cursor.execute(statement)
            logging.info("MariaDB table created.")
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")

    def load_csv(self, cursor, sql_file):
        logging.info(f"Loading {sql_file} data into MariaDB table...")
        file_path = SQL_DIR / sql_file
        try:
            with open(file_path, "r") as file:
                statement = file.read()
                cursor.execute(statement)
            logging.info("Data successfully loaded into MariaDB table.")
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")

    def close_connection(self):
        self.conn.close()