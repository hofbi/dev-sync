import yaml
from pathlib import Path

from devsync.data import BackupFolder, Target
from devsync.log import logger


class YMLConfigParser:
    def __init__(self, config):
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

    @staticmethod
    def parse_targets(short_dest_file: Path):
        content = YMLConfigParser.get_yaml_content(short_dest_file)
        if content:
            return {
                target["shortDest"]: target["destPath"]
                for target in content["shortDests"]
            }
        return {}

    @staticmethod
    def get_target_from_argument(short_dest_file: Path, target_arg):
        short_dest_file.touch()

        targets = YMLConfigParser.parse_targets(short_dest_file)
        if target_arg in targets:
            logger.info(
                f"Using shortcut {target_arg} as destination path to: {targets[target_arg]}\n"
            )
            return Target(targets[target_arg])
        return Target(target_arg)

    def parse_home(self):
        return self.__content["home"]
