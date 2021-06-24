import yaml
from pathlib import Path

from devsync.data import BackupFolder


class YMLConfigParser:
    def __init__(self, config: Path):
        self.__content = self.get_yaml_content(config)

    @staticmethod
    def get_yaml_content(filename: Path):
        return yaml.load(filename.read_bytes(), Loader=yaml.FullLoader)

    def parse_backup_folder(self):
        backup_folders = self.__content["backupFolder"]
        return [
            BackupFolder(self.parse_home(), element["path"])
            for element in backup_folders
        ]

    def parse_home(self):
        return self.__content["home"]
