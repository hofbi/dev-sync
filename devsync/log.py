import logging
import coloredlogs
import verboselogs
import os

from logging.handlers import TimedRotatingFileHandler
from devsync.config import LOGFILE, NAME


def init_logging():
    dev_sync_logger = verboselogs.VerboseLogger(NAME)

    log_dir = os.path.dirname(LOGFILE)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    coloredlogs.install(level='DEBUG', milliseconds=True, logger=dev_sync_logger)
    dev_sync_logger.setLevel(logging.DEBUG)

    fh = TimedRotatingFileHandler(LOGFILE, when="MIDNIGHT")
    fh.setFormatter(logging.Formatter(coloredlogs.DEFAULT_LOG_FORMAT))
    dev_sync_logger.addHandler(fh)

    return dev_sync_logger


logger = init_logging()
