import yaml
import os
import pathlib

from devsync.data import BackupFolder, Target
from devsync.log import logger


class YMLConfigParser:
    def __init__(self, config):
        self.__content = self.get_yaml_content(config)

    @staticmethod
    def get_yaml_content(filename):
        with open(filename, "r") as stream:
            return yaml.load(stream)

    def parse_backup_folder(self):
        backup_folders = self.__content["backupFolder"]
        return [
            BackupFolder(self.parse_home(), element["path"])
            for element in backup_folders
        ]

    @staticmethod
    def parse_targets(short_dest_file):
        content = YMLConfigParser.get_yaml_content(short_dest_file)
        if content:
            targets = content["shortDests"]
            return {target["shortDest"]: target["destPath"] for target in targets}

        return {}

    @staticmethod
    def get_target_from_argument(short_dest_file, target_arg):
        if not os.path.exists(short_dest_file):
            pathlib.Path(short_dest_file).touch()

        targets = YMLConfigParser.parse_targets(short_dest_file)
        if target_arg in targets:
            logger.info(
                'Using shortcut "{}" as destination path to: {}\n'.format(
                    target_arg, targets[target_arg]
                )
            )
            return Target(targets[target_arg])
        else:
            return Target(target_arg)

    def parse_home(self):
        return self.__content["home"]
