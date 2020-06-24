import unittest
import os

from unittest.mock import patch, MagicMock
from devsync.parser import YMLConfigParser
from devsync.config import SCRIPT_DIR


class YMLConfigParserTest(unittest.TestCase):
    CONFIG = os.path.join(SCRIPT_DIR, "config", "test_config.yml")
    SHORT_DEST = os.path.join(SCRIPT_DIR, "config", "test_shortdest.yml")

    def test_get_yaml_content_valid_file_not_empty(self):
        self.assertIsNotNone(
            YMLConfigParser.get_yaml_content(YMLConfigParserTest.CONFIG)
        )

    def test_get_yaml_content_invalid_file_error(self):
        with self.assertRaises(FileNotFoundError):
            YMLConfigParser.get_yaml_content("config/not_existing.yml")

    def test_parse_home_correct(self):
        parser = YMLConfigParser(YMLConfigParserTest.CONFIG)
        self.assertEqual("/home/user", parser.parse_home())

    def test_parse_backup_folder_correct(self):
        parser = YMLConfigParser(YMLConfigParserTest.CONFIG)
        self.assertEqual(3, len(parser.parse_backup_folder()))

    def test_parse_targets_valid_file_correct(self):
        self.assertEqual(
            2, len(YMLConfigParser.parse_targets(YMLConfigParserTest.SHORT_DEST))
        )

    @patch(
        "devsync.parser.YMLConfigParser.get_yaml_content", MagicMock(return_value=[])
    )
    def test_parse_targets__empty_file_correct(self):
        self.assertEqual(
            0, len(YMLConfigParser.parse_targets(YMLConfigParserTest.SHORT_DEST))
        )

    def test_get_target_from_argument_is_short_dest(self):
        self.assertEqual(
            "/tmp",
            YMLConfigParser.get_target_from_argument(
                YMLConfigParserTest.SHORT_DEST, "TEST"
            ).path,
        )

    def test_get_target_from_argument_regular_path(self):
        self.assertEqual(
            "/tmp",
            YMLConfigParser.get_target_from_argument(
                YMLConfigParserTest.SHORT_DEST, "/tmp"
            ).path,
        )
