from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import patch, MagicMock

from pathlib import Path

from devsync.log import init_logging


class LogTest(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_init_logging___logfile_path_does_not_exist__should_be_created(self):
        init_logging(Path("logs/logfile"))
        self.assertTrue(Path("logs/logfile").exists())
