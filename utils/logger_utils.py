import logging
import os
from utils.config import Config

def setup_logger(test_method_name, data_set_id):
    # Create logs directory if it doesn't exist
    log_dir = Config.LOG_DIR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create log file with the name of the test method and dataset id
    log_file = os.path.join(log_dir, f"{test_method_name}_data_set_{data_set_id}.log")

    # Configure the logger
    logger = logging.getLogger(f"{test_method_name}_data_set_{data_set_id}")
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create file handler which logs messages
    fh = logging.FileHandler(log_file, mode='w')  # Set mode to 'w' to overwrite the log file
    fh.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
