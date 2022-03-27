from pathlib import Path

from pyfakefs.fake_filesystem_unittest import TestCase

from devsync.parser import YMLConfigParser

CONFIG_CONTENT = """
home: /home/user                    # Source root folder
backupFolder:                       # Folders that should be saved (relative to "home" variable)
  - path: Pictures                  # Folder name
  - path: Documents
  - path: Development
"""


class YMLConfigParserTest(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

        self.config = Path("test_config.yml")
        self.fs.create_file(self.config, contents=CONFIG_CONTENT)

    def test_get_yaml_content_valid_file_not_empty(self):
        self.assertIsNotNone(YMLConfigParser.get_yaml_content(self.config))

    def test_get_yaml_content_invalid_file_error(self):
        with self.assertRaises(FileNotFoundError):
            YMLConfigParser.get_yaml_content(Path("config/not_existing.yml"))

    def test_parse_home_correct(self):
        parser = YMLConfigParser(self.config)
        self.assertEqual(Path("/home/user"), parser.parse_home())

    def test_parse_backup_folder_correct(self):
        parser = YMLConfigParser(self.config)
        self.assertEqual(3, len(parser.parse_backup_folder()))
