import subprocess
from pathlib import Path

from devsync.config import LOGFILE
from devsync.data import BackupFolder, Repo, Target
from devsync.log import logger
from devsync.parser import YMLConfigParser


def run_backup(parser: YMLConfigParser, target: Target, last_update: int, report: bool):
    home = parser.parse_home()

    backup_folders = parser.parse_backup_folder()
    for backup_folder in backup_folders:
        backup_folder.find_repos_in_path()

    if target.is_relative_to(home):
        logger.notice("Target is relative to root. Updating local repos only.")
        target = Target(home)

    logger.info("Updating Repos...\n")
    repo_sync = RepoSync(home, backup_folders)
    repo_sync.update_repos(target, last_update, report)

    if target.path == home:
        logger.info("Target is relative to root. Updated only the local repos")
        return

    logger.info("Sync data with rsync...\n")
    rsync = RSync(home, backup_folders)
    rsync.sync(target, report)


class RSync:
    OPTIONS = (
        "-a",  # Make 1 to 1 copy
        "-v",  # Verbose
        "--whole-file",  # Copy whole file without delta algorithm
        "--delete",  # Delete if not existing in root
        "--stats",  # Show file transfer stats
        "--progress",  # Show Progress
        "--modify-window=2",  # Allowing times to differ by up to 2 seconds. Related to FAT 2 second
        # resolution for timestamps
        f"--log-file={LOGFILE}",  # Log to LOGFILE
    )

    def __init__(self, root: Path, backup_folders: list[BackupFolder]):
        self.__root = root
        self.__backup_folders = backup_folders

    @staticmethod
    def get_options(report: bool, excludes: list[Path]) -> str:
        options = list(RSync.OPTIONS)
        if report:
            options.append("-n")  # Rsync Dry Run

        options.extend([f'--exclude="{path}"' for path in excludes])

        return " ".join(options)

    def sync(self, target: Target, report: bool) -> None:
        for element in self.__backup_folders:
            excludes = element.get_relative_repo_paths()
            options = self.get_options(report, excludes)

            logger.verbose(f"{len(excludes)} Repos to exclude in {element.path}")
            logger.debug(
                f"Running Rsync\n\tSource: {element.path}\n\tTarget: {target.path}\n"
                f"\tOptions: {options}\n"
            )
            subprocess.check_call(
                f"rsync {options} {element.path} {target.path}",
                shell=True,
                cwd=self.__root,
            )
            # TODO: Remove shell=True but check rsync excludes work


class RepoSync:
    def __init__(self, root: Path, backup_folders: list[BackupFolder]):
        self.__root = root
        self.__backup_folders = backup_folders

    def update_repos(self, target: Target, last_update: int, report: bool):
        all_repos = self.get_all_repos()
        logger.verbose(f"{len(all_repos)} repos found in all paths")

        all_repos = [repo for repo in all_repos if repo.is_update_required(last_update)]
        logger.verbose(f"{len(all_repos)} repos to update on target {target.path}\n")

        for repo in all_repos:
            repo.update_repo_on_target(self.__root, target, report)

    def get_all_repos(self) -> list[Repo]:
        all_repos = []
        for element in self.__backup_folders:
            repos = element.repos
            logger.verbose(f"--> {len(repos)} repos found in path {element.path}")
            all_repos.extend(repos)

        return all_repos
