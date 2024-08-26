
import logging.config
import sys


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger