import logging
from logging import Formatter, Logger
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import colorlog

from dev_sync.config import LOGFILE, NAME


def init_logging(logfile: Path) -> Logger:
    logfile.parent.mkdir(exist_ok=True, parents=True)

    common_log_format = "%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"

    stream_handler = colorlog.StreamHandler()
    stream_handler.setFormatter(colorlog.ColoredFormatter("%(log_color)s" + common_log_format))

    file_handler = TimedRotatingFileHandler(logfile, when="MIDNIGHT")
    file_handler.setFormatter(Formatter(common_log_format))

    dev_sync_logger = logging.getLogger(NAME)
    dev_sync_logger.setLevel(logging.DEBUG)
    dev_sync_logger.addHandler(stream_handler)
    dev_sync_logger.addHandler(file_handler)

    return dev_sync_logger


logger = init_logging(LOGFILE)
