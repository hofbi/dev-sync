from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from devsync.parser import YMLConfigParser

CONFIG_CONTENT = """
home: /home/user                    # Source root folder
backupFolder:                       # Folders that should be saved (relative to "home" variable)
  - path: Pictures                  # Folder name
  - path: Documents
  - path: Development
"""


def test_get_yaml_content_valid_file_not_empty(fs: FakeFilesystem):
    config = Path("test_config.yml")
    fs.create_file(config, contents=CONFIG_CONTENT)
    assert YMLConfigParser.get_yaml_content(config) is not None


def test_get_yaml_content_invalid_file_error():
    with pytest.raises(FileNotFoundError):
        YMLConfigParser.get_yaml_content(Path("config/not_existing.yml"))


def test_parse_home_correct(fs: FakeFilesystem):
    config = Path("test_config.yml")
    fs.create_file(config, contents=CONFIG_CONTENT)
    parser = YMLConfigParser(config)
    assert parser.parse_home() == Path("/home/user")


EXPECTED_BACKUP_FOLDER_COUNT = 3


def test_parse_backup_folder_correct(fs: FakeFilesystem):
    config = Path("test_config.yml")
    fs.create_file(config, contents=CONFIG_CONTENT)
    parser = YMLConfigParser(config)
    assert len(parser.parse_backup_folder()) == EXPECTED_BACKUP_FOLDER_COUNT
