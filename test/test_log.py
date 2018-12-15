import unittest

from unittest.mock import patch, MagicMock
from devsync.log import init_logging


class LogTest(unittest.TestCase):

    @patch('devsync.log.os')
    @patch('devsync.log.logging.handlers.TimedRotatingFileHandler.__init__', MagicMock(return_value=None))
    def test_init_logging_create_log_dir_if_not_existing(self, mock_os):
        mock_os.path.exists.return_value = False
        init_logging()
        self.assertTrue(mock_os.mkdir.called)

    @patch('devsync.log.os')
    @patch('devsync.log.logging.handlers.TimedRotatingFileHandler.__init__', MagicMock(return_value=None))
    def test_init_logging_create_no_log_dir_if_already_existing(self, mock_os):
        mock_os.path.exists.return_value = True
        init_logging()
        self.assertFalse(mock_os.mkdir.called)
