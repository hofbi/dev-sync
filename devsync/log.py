import logging
import coloredlogs
from pathlib import Path

from verboselogs import VerboseLogger
from logging.handlers import TimedRotatingFileHandler
from devsync.config import LOGFILE, NAME


def init_logging(logfile: Path) -> VerboseLogger:
    dev_sync_logger = VerboseLogger(NAME)

    logfile.parent.mkdir(exist_ok=True, parents=True)

    coloredlogs.install(level="DEBUG", milliseconds=True, logger=dev_sync_logger)
    dev_sync_logger.setLevel(logging.DEBUG)

    fh = TimedRotatingFileHandler(logfile, when="MIDNIGHT")
    fh.setFormatter(logging.Formatter(coloredlogs.DEFAULT_LOG_FORMAT))
    dev_sync_logger.addHandler(fh)

    return dev_sync_logger


logger = init_logging(LOGFILE)
