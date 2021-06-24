import os
import abc
import git
import datetime
import subprocess
from pathlib import Path
from typing import List

from devsync.log import logger


class Repo:
    def __init__(self, path):
        self.__path = path

    @property
    def path(self):
        return self.__path

    def is_update_required(self, last_update):
        return self.get_latest_commit_time > last_update

    def print_update_report(self):
        logger.debug(
            "Updating "
            + self.repo_type
            + " Repo "
            + self.path
            + " --> Last Commit "
            + str(datetime.datetime.utcfromtimestamp(self.get_latest_commit_time))
        )

    def get_repo_target_path(self, root, target):
        relative_path = self.path.replace(root, "")
        return os.path.join(target.path, relative_path)

    def update_repo_on_target(self, root, target, report):
        self.print_update_report()
        target_path = self.get_repo_target_path(root, target)
        if os.path.exists(target_path):
            logger.debug("\tFound on target {} --> pull\n".format(target_path))
            if not report:
                self.pull_repo(target_path)
        else:
            url = self.get_clone_url()
            logger.debug(
                "\tNot Found on target --> clone from {} into {}\n".format(
                    url, target_path
                )
            )
            if not report:
                self.clone_repo(url, target_path)

    @property
    @abc.abstractmethod
    def repo_type(self):
        raise NotImplementedError("Don't call me, I am abstract")

    @property
    @abc.abstractmethod
    def get_latest_commit_time(self):
        raise NotImplementedError("Don't call me, I am abstract")

    @abc.abstractmethod
    def pull_repo(self, target_path):
        raise NotImplementedError("Don't call me, I am abstract")

    @abc.abstractmethod
    def clone_repo(self, url, target_path):
        raise NotImplementedError("Don't call me, I am abstract")

    @abc.abstractmethod
    def get_clone_url(self):
        raise NotImplementedError("Don't call me, I am abstract")


class GitRepo(Repo):
    def get_clone_url(self):
        output = subprocess.check_output(
            "git remote get-url origin", shell=True, cwd=self.path
        )
        return output.decode("utf-8").split("\n")[0]

    def clone_repo(self, url, target_path):
        class CloneProgress(git.RemoteProgress):
            def line_dropped(self, line):
                print(line)

        git.Repo.clone_from(url, target_path, progress=CloneProgress())

    def pull_repo(self, target_path):
        subprocess.check_call(
            "git fetch && git reset --hard HEAD", shell=True, cwd=target_path
        )

    @property
    def repo_type(self):
        return "Git"

    @property
    def get_latest_commit_time(self):
        git_repo = git.Repo(self.path)
        heads_commit_time = [head.commit.committed_date for head in git_repo.heads]
        return max(heads_commit_time)


class HgRepo(Repo):
    def get_clone_url(self):
        output = subprocess.check_output("hg paths", shell=True, cwd=self.path)
        for item in output.decode("utf-8").split("\n"):
            if "default" in item:
                return self.parse_remote(item)

    def clone_repo(self, url, target_path):
        target_path = os.path.abspath(os.path.join(target_path, ".."))
        subprocess.check_call("hg clone " + url, shell=True, cwd=target_path)

    def pull_repo(self, target_path):
        subprocess.check_call("hg pull && hg up", shell=True, cwd=target_path)

    @property
    def repo_type(self):
        return "Hg"

    @property
    def get_latest_commit_time(self):
        output = subprocess.check_output("hg heads", shell=True, cwd=self.path)
        for item in output.decode("utf-8").split("\n"):
            if "date:" in item:
                return self.parse_date(item)

    @staticmethod
    def parse_date(item):
        date_str = item[5:].lstrip()
        date = datetime.datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
        return date.timestamp()

    @staticmethod
    def parse_remote(item):
        return item[len("default = ") :].lstrip()  # noqa E203 (conflicts with black)


class Target:
    def __init__(self, destination_path):
        self.__path = str(Path(destination_path).absolute())
        self.check_destination()

    @property
    def path(self):
        return self.__path

    def check_destination(self):
        if not Path(self.path).exists():
            raise FileNotFoundError("Target dir {} does not exist".format(self.path))

    def is_relative_to(self, other):
        try:
            Path(self.path).relative_to(other)
        except Exception:
            return False
        return True


class BackupFolder:
    def __init__(self, root: Path, path: str):
        self.__path = root / path
        self.__repos = []

    @property
    def repos(self) -> List[Repo]:
        return self.__repos

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def has_repos(self) -> bool:
        return bool(self.repos)

    def get_relative_repo_paths(self) -> List[str]:
        return [repo.path.replace(str(self.path) + "/", "") for repo in self.repos]

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
