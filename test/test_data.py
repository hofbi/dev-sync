import unittest
from pyfakefs.fake_filesystem_unittest import TestCase
import os

from pathlib import Path

from devsync.data import BackupFolder, HgRepo, Repo, GitRepo, Target


class TargetTest(unittest.TestCase):
    def test_constructor_absolute_destination_path(self):
        self.assertEqual("/tmp", Target("/tmp").path)

    def test_constructor_relative_destination_path(self):
        self.assertEqual(os.path.abspath("config"), Target("config").path)

    def test_constructor_not_existing_destination_path(self):
        with self.assertRaises(FileNotFoundError):
            Target("blub")

    def test_is_relative_to__other_not_relative__should_be_false(self):
        unit = Target("/tmp")
        self.assertFalse(unit.is_relative_to("/etc"))

    def test_is_relative_to__other_relative__should_be_true(self):
        unit = Target("/tmp")
        self.assertTrue(unit.is_relative_to("/tmp/"))

    def test_is_relative_to__other_same__should_be_true(self):
        unit = Target("/tmp")
        self.assertTrue(unit.is_relative_to("/tmp"))


class SaveDataTest(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def create_git_repo_in_path(self, path: Path):
        self.fs.create_dir(path / ".git")

    def test_constructor(self):
        backup_folder = BackupFolder(Path("/home/user"), "test")
        self.assertEqual(Path("/home/user/test"), backup_folder.path)
        self.assertFalse(backup_folder.repos)
        self.assertFalse(backup_folder.has_repos)

    def test_get_relative_repo_paths_with_no_repos_should_be_empty(self):
        backup_folder = BackupFolder(Path("/home/user"), "test")
        backup_folder.find_repos_in_path()

        repos = backup_folder.get_relative_repo_paths()

        self.assertFalse(repos)

    def test_get_relative_repo_paths_with_one_repo_should_be_only_repo_folder_name(
        self,
    ):
        self.create_git_repo_in_path(Path("/home/user/test/repo"))
        backup_folder = BackupFolder(Path("/home/user"), "test")
        backup_folder.find_repos_in_path()

        repos = backup_folder.get_relative_repo_paths()

        self.assertListEqual(["repo"], repos)

    def test_find_repos_in_path_with_no_repos_should_be_empty(self):
        backup_folder = BackupFolder(Path("/home/user"), "test")
        backup_folder.find_repos_in_path()
        self.assertFalse(backup_folder.has_repos)
        self.assertFalse(backup_folder.repos)

    def test_find_repos_in_path_with_one_repo_in_and_one_out_of_path_should_be_one_repo(
        self,
    ):
        self.create_git_repo_in_path(Path("/home/user/test/repo_in"))
        self.create_git_repo_in_path(Path("/home/user/repo_out"))
        backup_folder = BackupFolder(Path("/home/user"), "test")

        backup_folder.find_repos_in_path()

        self.assertEqual("/home/user/test/repo_in", backup_folder.repos[0].path)
        self.assertTrue(backup_folder.has_repos)


class RepoTest(unittest.TestCase):
    def test_constructor(self):
        repo = Repo("/tmp")
        self.assertEqual("/tmp", repo.path)

    def test_get_repo_target_path_correct(self):
        repo = Repo("/foo/blub")
        self.assertEqual(
            "/tmp/blub", repo.get_repo_target_path("/foo/", Target("/tmp"))
        )


class HgRepoTest(unittest.TestCase):
    HG_HEADS_DATE_LINE = "date:        Mon Nov 19 10:37:51 2018 +0100"
    HG_PATHS_DEFAULT_LINE = "default = https://server.com/user/repo"

    def test_parse_date_valid(self):
        self.assertEqual(1542620271, HgRepo.parse_date(HgRepoTest.HG_HEADS_DATE_LINE))

    def test_parse_remote_valid(self):
        self.assertEqual(
            "https://server.com/user/repo",
            HgRepo.parse_remote(HgRepoTest.HG_PATHS_DEFAULT_LINE),
        )

    def test_get_repo_type_hg(self):
        repo = HgRepo("")
        self.assertEqual("Hg", repo.repo_type)


class GitRepoTest(unittest.TestCase):
    def test_get_repo_type_git(self):
        repo = GitRepo("")
        self.assertEqual("Git", repo.repo_type)
