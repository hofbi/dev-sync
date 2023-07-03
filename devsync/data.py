import abc
import datetime
import os
import re
import subprocess
from pathlib import Path

import git

from devsync.log import logger


class Target:
    def __init__(self, destination_path: str | Path):
        self.__path = Path(destination_path).absolute()
        self.check_destination()

    @property
    def path(self) -> Path:
        return self.__path

    def check_destination(self) -> None:
        if not Path(self.path).exists():
            msg = f"Target dir {self.path} does not exist"
            raise FileNotFoundError(msg)

    def is_relative_to(self, other) -> bool:
        try:
            Path(self.path).relative_to(other)
        except ValueError:
            return False
        return True


class Repo:
    def __init__(self, path: str):
        self.__path = Path(path)

    @property
    def path(self) -> Path:
        return self.__path

    def is_update_required(self, last_update) -> bool:
        return self._get_latest_commit_time > last_update

    def __print_update_report(self) -> None:
        logger.debug(
            f"Updating {self.repo_type} Repo {self.path} --> Last Commit "
            f"{datetime.datetime.utcfromtimestamp(self._get_latest_commit_time)}"
        )

    def get_repo_target_path(self, root, target: Target) -> Path:
        return target.path / self.path.relative_to(root)

    def update_repo_on_target(self, root: Path, target: Target, report: bool):
        self.__print_update_report()
        target_path = self.get_repo_target_path(root, target)
        if target_path.exists():
            logger.debug(f"\tFound on target {target_path} --> pull\n")
            if not report:
                self._pull_repo(target_path)
        else:
            url = self._get_clone_url()
            logger.debug(
                f"\tNot Found on target --> clone from {url} into {target_path}\n"
            )
            if not report:
                self._clone_repo(url, target_path)

    @property
    @abc.abstractmethod
    def repo_type(self) -> str:
        msg = "Don't call me, I am abstract"
        raise NotImplementedError(msg)

    @property
    @abc.abstractmethod
    def _get_latest_commit_time(self) -> float:
        msg = "Don't call me, I am abstract"
        raise NotImplementedError(msg)

    @abc.abstractmethod
    def _pull_repo(self, target_path: Path) -> None:
        msg = "Don't call me, I am abstract"
        raise NotImplementedError(msg)

    @abc.abstractmethod
    def _clone_repo(self, url: str, target_path: Path) -> None:
        msg = "Don't call me, I am abstract"
        raise NotImplementedError(msg)

    @abc.abstractmethod
    def _get_clone_url(self) -> str:
        msg = "Don't call me, I am abstract"
        raise NotImplementedError(msg)


class GitRepo(Repo):
    def _get_clone_url(self) -> str:
        output = subprocess.check_output(
            "git remote get-url origin", shell=True, cwd=self.path
        )
        return output.decode("utf-8").split("\n", maxsplit=1)[0]

    def _clone_repo(self, url: str, target_path: Path) -> None:
        class CloneProgress(git.RemoteProgress):
            def line_dropped(self, line):
                print(line)

        git.Repo.clone_from(url, target_path, progress=CloneProgress())

    def _pull_repo(self, target_path: Path) -> None:
        main_branch = GitRepo.get_default_branch(target_path)
        subprocess.check_call(
            f"git fetch --all --prune && git reset --hard origin/{main_branch}",
            shell=True,
            cwd=target_path,
        )

    @property
    def repo_type(self) -> str:
        return "Git"

    @property
    def _get_latest_commit_time(self) -> float:
        git_repo = git.Repo(self.path)
        heads_commit_time = [head.commit.committed_date for head in git_repo.heads]
        return max(heads_commit_time)

    @staticmethod
    def get_default_branch(target_path: Path) -> str:
        try:
            origin_info = subprocess.check_output(
                "git remote show origin",
                shell=True,
                cwd=target_path,
                env={**os.environ, "LANG": "en_US.UTF-8"},
            ).decode("utf-8")
        except subprocess.CalledProcessError:
            return "master"
        default_branch = re.search(r"HEAD branch:\s(\w*)", origin_info, re.DOTALL)
        return default_branch.group(1) if default_branch else "master"


class HgRepo(Repo):
    def _get_clone_url(self) -> str:
        output = subprocess.check_output("hg paths", shell=True, cwd=self.path)
        for item in output.decode("utf-8").split("\n"):
            if "default" in item:
                return self.parse_remote(item)
        return ""

    def _clone_repo(self, url: str, target_path: Path) -> None:
        subprocess.check_call(
            "hg clone " + url, shell=True, cwd=target_path.parent.absolute()
        )

    def _pull_repo(self, target_path: Path) -> None:
        subprocess.check_call("hg pull && hg up", shell=True, cwd=target_path)

    @property
    def repo_type(self) -> str:
        return "Hg"

    @property
    def _get_latest_commit_time(self) -> float:
        output = subprocess.check_output("hg heads", shell=True, cwd=self.path)
        for item in output.decode("utf-8").split("\n"):
            if "date:" in item:
                return self.parse_date(item)
        return 0

    @staticmethod
    def parse_date(item: str) -> float:
        date_str = item[5:].lstrip()
        date = datetime.datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
        return date.timestamp()

    @staticmethod
    def parse_remote(item: str):
        return item[len("default = ") :].lstrip()


class BackupFolder:
    def __init__(self, root: Path, path: str):
        self.__path = root / path
        self.__repos: list[Repo] = []

    @property
    def repos(self) -> list[Repo]:
        return self.__repos

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def has_repos(self) -> bool:
        return bool(self.repos)

    def get_relative_repo_paths(self) -> list[Path]:
        return [repo.path.relative_to(self.path) for repo in self.repos]

    def find_repos_in_path(self) -> None:
        for root, dirs, _ in os.walk(self.path, topdown=True):
            dirs.sort()
            if ".git" in dirs:
                self.__repos.append(GitRepo(root))
                dirs[:] = []
            elif ".hg" in dirs:
                self.__repos.append(HgRepo(root))
                dirs[:] = []
            elif ".svn" in dirs:
                dirs[:] = []
