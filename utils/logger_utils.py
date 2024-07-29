
import logging
import os
from utils.config import Config

def setup_logger(test_method_name, data_set_id):
    environment = os.getenv('ENVIRONMENT', 'default')
    if environment == 'default':
        print("Debug: Environment variable not set, using default")  # Debug print

    log_dir = os.path.join(Config.LOG_DIR, environment, test_method_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    data_set_dir = os.path.join(log_dir, f"data_set_{data_set_id}")
    if not os.path.exists(data_set_dir):
        os.makedirs(data_set_dir)

    log_file = os.path.join(data_set_dir, f"{test_method_name}_data_set_{data_set_id}.log")

    logger = logging.getLogger(f"{test_method_name}_data_set_{data_set_id}")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    fh = logging.FileHandler(log_file, mode='w')  # Set mode to 'w' to overwrite the log file
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
