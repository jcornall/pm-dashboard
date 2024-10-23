from threading import Thread
from src.tenable.credentials import TenableCredentials
from src.tenable.export_assets import export_tenable_assets
from src.tenable.export_vulnerabilities import export_tenable_vulnerabilities
from src.tenable.load_assets import load_tenable_assets
from src.tenable.load_vulnerabilities import load_tenable_vulnerabilities
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

    t1 = Thread(target=__process_vulnerabilities, args=(creds,))
    t2 = Thread(target=__process_assets, args=(creds,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    logging.info("Program execution successful, exiting program.")


def __process_vulnerabilities(creds: TenableCredentials):
    logging.info("Exporting vulnerabilities...")
    export = export_tenable_vulnerabilities(creds)
    logging.info("Loading exported vulnerabilities into database...")
    load_tenable_vulnerabilities(export)


def __process_assets(creds: TenableCredentials):
    logging.info("Exporting assets...")
    export = export_tenable_assets(creds)
    logging.info("Loading exported assets into database...")
    load_tenable_assets(export)
