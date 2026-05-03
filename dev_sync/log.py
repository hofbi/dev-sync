import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import coloredlogs

from dev_sync.config import LOGFILE, NAME


def init_logging(logfile: Path) -> Logger:
    dev_sync_logger = logging.getLogger(NAME)

    logfile.parent.mkdir(exist_ok=True, parents=True)

    coloredlogs.install(level="DEBUG", milliseconds=True, logger=dev_sync_logger)
    dev_sync_logger.setLevel(logging.DEBUG)

    file_handler = TimedRotatingFileHandler(logfile, when="MIDNIGHT")
    file_handler.setFormatter(logging.Formatter(coloredlogs.DEFAULT_LOG_FORMAT))
    dev_sync_logger.addHandler(file_handler)

    return dev_sync_logger


logger = init_logging(LOGFILE)
