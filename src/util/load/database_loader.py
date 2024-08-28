#!/usr/bin/env python3.12
#-*- coding: utf-8 -*-
"""This module defines the DatabaseLoader class, used to load processed data into the MariaDB database.
"""

from src.config.transform_config import *
from src.config.constants import *
from pathlib import Path
import pandas as pd
import re
import json
import mariadb
import sys


class DatabaseLoader():

    def __init__(self, export_type, connection_parameters):
        """Instantiate a DatabaseLoader object."""
        self.conn = self.connect_to_database(connection_parameters)
        self.export_type = export_type
        self.cursor = self.set_cursor(self.conn)

    def connect_to_database(self, connection_parameters):
        """Connect to MariaDB using the supplied credentials."""
        logging.info(f"Connecting to {connection_parameters["host"]} as {connection_parameters["user"]}...")
        try:
            conn = mariadb.connect(**connection_parameters)
            logging.info(f"Successfully connected to {connection_parameters["host"]}.")
            return conn
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")
            sys.exit(1)

    def set_cursor(self, conn):
        """Sets a cursor object, providing an interface with the MariaDB database."""
        cursor = conn.cursor()
        return cursor

    def drop_table(self, cursor, database, table):
        """Executes a DROP TABLE statement."""
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

    def create_table(self, cursor, file_path, sql_file):
        """Executes a CREATE TABLE statement."""
        logging.info("Creating new MariaDB table...")
        sql_file_path = Path(file_path) / sql_file
        try:
            with open(sql_file_path, "r") as file:
                statement = file.read()
                cursor.execute(statement)
            logging.info("MariaDB table created.")
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")

    def load_csv(self, cursor, file_path, sql_file):
        """Executes a LOAD DATA statement."""
        logging.info(f"Loading {sql_file} data into MariaDB table...")
        sql_file_path = Path(file_path) / sql_file
        try:
            with open(sql_file_path, "r") as file:
                statement = file.read()
                cursor.execute(statement)
            logging.info("Data successfully loaded into MariaDB table.")
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")

    def insert_into_table(self, cursor, file_path, sql_file):
        """Executes an INSERT INTO statement."""
        logging.info(f"Inserting data into MariaDB table...")
        sql_file_path = Path(file_path) / sql_file
        try:
            with open(sql_file_path, "r") as file:
                statement = file.read()
                cursor.execute(statement)
            logging.info("Data successfully inserted into MariaDB table.")
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")

    def delete_from_table(self, cursor, file_path, sql_file):
        """Executes a DELETE FROM statement."""
        logging.info(f"Deleting data from MariaDB table...")
        sql_file_path = Path(file_path) / sql_file
        try:
            with open(sql_file_path, "r") as file:
                statement = file.read()
                cursor.execute(statement)
            logging.info("Data successfully delete from MariaDB table.")
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")

    def select_count(self, cursor, file_path, sql_file):
        """Executes a SELECT * statement and logs a count of the results."""
        logging.info(f"Selecting data from MariaDB table...")
        sql_file_path = Path(file_path) / sql_file
        try:
            with open(sql_file_path, "r") as file:
                statement = file.read()
                for result in cursor.execute(statement):
                    logging.info(f"{result.statement}")
                    logging.info(f"{result.rowcount}")
            logging.info("Data successfully selected from MariaDB table.")
        except mariadb.Error as e:
            logging.warning(f"Error: {e}.")

    def close_connection(self):
        """Closes the connection to the MariaDB database."""
        self.conn.close()