import logging
import sys
import csv
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    # StreamHandler for console output
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handler)

    return logger

def get_csv_logger():
    logger = logging.getLogger("csv_logger")
    logger.setLevel(logging.INFO)
    load_dotenv()
    log_file = os.path.normpath(os.getenv("LOG_PATH"))
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    if not os.path.exists(log_file):
        fieldnames = ",".join([
            'timestamp', 'user_id', 'username', 'first_name', 'last_name',
            'is_premium', 'app_language', 'action', 'action_details'
        ])
        with open(log_file, 'w') as file:
            file.write(f"{fieldnames}\n")

    handler = TimedRotatingFileHandler(log_file, when="W0", interval=1, backupCount=100)
    formatter = logging.Formatter('%(asctime)s,%(message)s', datefmt='%Y-%m-%d')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger