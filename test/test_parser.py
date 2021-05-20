from pyfakefs.fake_filesystem_unittest import TestCase

from pathlib import Path

from devsync.parser import YMLConfigParser


CONFIG_CONTENT = """
home: /home/user                    # Source root folder
backupFolder:                       # Folders that should be saved (relative to "home" variable)
  - path: Pictures                  # Folder name
  - path: Documents
  - path: Development
"""


SHORT_DEST_CONTENT = """
shortDests:                         # Destination Shortcuts
  - shortDest: TEST                 # Destination name (selectable by CLI argument)
    destPath: /tmp                  # Root path of destination
  - shortDest: USB
    destPath: /media/user/usbdevice
"""


class YMLConfigParserTest(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

        self.config = Path("test_config.yml")
        self.short_dest = Path("test_shortdest.yml")

        self.fs.create_file(self.config, contents=CONFIG_CONTENT)
        self.fs.create_file(self.short_dest, contents=SHORT_DEST_CONTENT)

    def test_get_yaml_content_valid_file_not_empty(self):
        self.assertIsNotNone(YMLConfigParser.get_yaml_content(self.config))

    def test_get_yaml_content_invalid_file_error(self):
        with self.assertRaises(FileNotFoundError):
            YMLConfigParser.get_yaml_content(Path("config/not_existing.yml"))

    def test_parse_home_correct(self):
        parser = YMLConfigParser(self.config)
        self.assertEqual("/home/user", parser.parse_home())

    def test_parse_backup_folder_correct(self):
        parser = YMLConfigParser(self.config)
        self.assertEqual(3, len(parser.parse_backup_folder()))

    def test_parse_targets_valid_file_correct(self):
        self.assertEqual(2, len(YMLConfigParser.parse_targets(self.short_dest)))

    def test_parse_targets__empty_file_correct(self):
        empty_path = Path("empty.yml")
        self.fs.create_file(empty_path)
        self.assertEqual(0, len(YMLConfigParser.parse_targets(empty_path)))

    def test_get_target_from_argument_is_short_dest(self):
        self.assertEqual(
            "/tmp",
            YMLConfigParser.get_target_from_argument(self.short_dest, "TEST").path,
        )

    def test_get_target_from_argument_regular_path(self):
        self.assertEqual(
            "/tmp",
            YMLConfigParser.get_target_from_argument(self.short_dest, "/tmp").path,
        )
