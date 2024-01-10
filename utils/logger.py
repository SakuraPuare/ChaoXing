import logging
from logging import config

from tqdm import tqdm


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except:
            self.handleError(record)


class Formatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s][%(asctime)s][%(processName)s][%(levelname)s](%(filename)s:%(lineno)d) %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


LOGGING_CONFIG = {
    "version": 1,
    'loggers': {
        'httpx': {
            'level': 'WARNING',
        },
        'httpcore': {
            'level': 'WARNING',
        },
    },
}

config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger('ChaoXing')
logger.setLevel(logging.INFO)

ch = TqdmLoggingHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(Formatter())
logger.addHandler(ch)
