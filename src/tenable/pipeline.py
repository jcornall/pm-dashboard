from src.tenable.credentials import TenableCredentials
from src.tenable.export_assets import export_tenable_assets
from src.tenable.export_vulnerabilities import export_tenable_vulnerabilities
from src.util.extract.api_export import *
from src.util.transform.data_processor import *
from src.util.load.database_loader import *
from src.config.transform_config import *
from src.config.constants import *
from src.config.extract_config import *
from src.config.logger_config import *


def tenable():
    """
    Runs the pipeline for extracting tenable data from the API, processing them,
    and loading the extracted data into the database.
    """

    creds = TenableCredentials(
        access_key=os.getenv("TENABLE_ACCESS_KEY"),
        secret_key=os.getenv("TENABLE_SECRET_KEY"),
    )

    # Setup
    print(f"Current Working Directory: {Path.cwd()}")
    set_up_logger()
    logging.info("Logger setup successful.")
    purge_old_files(DATA_DIR)
    purge_old_files(LOGS_DIR)
    logging.info("Old data purge successful...")
    purge_empty_dirs(DATA_DIR)
    purge_empty_dirs(LOGS_DIR)
    logging.info("Empty data directory purge successful...")
    logging.info("Data extraction successful.")
    set_up_file_structure()
    logging.info("File structure setup successful.")

    # Extract
    logging.info("Starting data extraction...")
    export_tenable_vulnerabilities(creds)
    logging.info("Vulnerability data extraction successful...")
    export_tenable_assets(creds)
    logging.info("Asset data extraction successful...")

    # Transform
    logging.info("Starting data transformation...")
    purge_dir(PROCESSED_DIR)
    process_data(VULN_EXPORT_DIR)
    process_data(ASSET_EXPORT_DIR)
    logging.info("Data transformation successful.")

    # Load
    logging.info("Starting data loading...")
    load_data("vulnerabilities", "create_vuln_table.txt", "load_vuln_csv.txt")

    logging.info("Program execution successful, exiting program.")


def process_data(file_path):
    """Sequence DataProcessor calls to DataProcessor."""
    data_processor = DataProcessor(file_path)
    data_processor.transform_data(
        data_processor.dir_path, data_processor.header_file, data_processor.export_type
    )
    # configure_data_processor(data_processor)
    return 0


def configure_data_processor(data_processor):
    """Configure the DataProcessor by generating new YAML files containing all JSON data headers."""
    generate_header_yaml(data_processor)


def load_data(table, create_statement, load_statement):
    """Load the data into a MariaDB database."""
    database_loader = DatabaseLoader(table, CONN_PARAMS)
    database_loader.drop_table(database_loader.cursor, "tenable", table)
    database_loader.create_table(database_loader.cursor, create_statement)
    database_loader.load_csv(database_loader.cursor, load_statement)
    database_loader.conn.commit()
    database_loader.cursor.close()
    database_loader.close_connection()
