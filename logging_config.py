import logging.config
from pythonjsonlogger import jsonlogger

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s %(module)s",
        }
    },
    "handlers": {
        "stdout": {
            "stream": "ext://sys.stdout",
            "formatter": "json",
        }
    },
    "loggers": {"": {"handlers": ["stdout"], "level": "WARN"}},
}


logging.config.dictConfig(LOGGING)