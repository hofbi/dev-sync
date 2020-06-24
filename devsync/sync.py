import copy
import subprocess

from devsync.log import logger
from devsync.config import LOGFILE


def run_backup(parser, target, last_update, report):
    home = parser.parse_home()
    backup_folders = parser.parse_backup_folder()

    for backup_folder in backup_folders:
        backup_folder.find_repos_in_path()

    logger.info("Updating Repos...\n")
    repo_sync = RepoSync(home, backup_folders)
    repo_sync.update_repos(target, last_update, report)

    logger.info("Sync data with rsync...\n")
    rsync = RSync(home, backup_folders)
    rsync.sync(target, report)


class RSync:
    OPTIONS = [
        "-a",  # Make 1 to 1 copy
        "-v",  # Verbose
        "--whole-file",  # Copy whole file without delta algorithm
        "--delete",  # Delete if not existing in root
        "--stats",  # Show file transfer stats
        "--progress",  # Show Progress
        "--modify-window=2",  # Allowing times to differ by up to 2 seconds. Related to FAT 2 second
        # resolution for timestamps
        "--log-file={}".format(LOGFILE),  # Log to LOGFILE
    ]

    def __init__(self, root, backup_folders):
        self.__root = root
        self.__backup_folders = backup_folders

    @staticmethod
    def get_options(report, excludes):
        options = copy.deepcopy(RSync.OPTIONS)
        if report:
            options.append("-n")  # Rsync Dry Run
        for path in excludes:
            options.append('--exclude="{}"'.format(path))

        return " ".join(options)

    def sync(self, target, report):
        for element in self.__backup_folders:
            excludes = element.get_relative_repo_paths()
            options = self.get_options(report, excludes)

            logger.verbose(str(len(excludes)) + " Repos to exclude in " + element.path)
            logger.debug(
                "Running Rsync"
                + "\n\tSource: "
                + element.path
                + "\n\tTarget: "
                + target.path
                + "\n\tOptions: "
                + options
                + "\n"
            )
            subprocess.check_call(
                "rsync {} {} {}".format(options, element.path, target.path),
                shell=True,
                cwd=self.__root,
            )


class RepoSync:
    def __init__(self, root, backup_folders):
        self.__root = root
        self.__backup_folders = backup_folders

    def update_repos(self, target, last_update, report):
        all_repos = self.get_all_repos()
        logger.verbose(str(len(all_repos)) + " Repos found in all paths")

        all_repos = [repo for repo in all_repos if repo.is_update_required(last_update)]
        logger.verbose(
            "{} Repos to update on target {}\n".format(len(all_repos), target.path)
        )

        for repo in all_repos:
            repo.update_repo_on_target(self.__root, target, report)

    def get_all_repos(self):
        all_repos = []
        for element in self.__backup_folders:
            repos = element.repos
            logger.verbose(
                "--> " + str(len(repos)) + " Repos found in path " + element.path
            )
            all_repos.extend(repos)

        return all_repos
