import unittest
import os

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


class SaveDataTest(unittest.TestCase):
    def test_constructor(self):
        backup_folder = BackupFolder("/home/user", "test")
        self.assertEqual("/home/user/test", backup_folder.path)
        self.assertFalse(backup_folder.repos)
        self.assertFalse(backup_folder.has_repos)

    def test_get_relative_repo_paths_no_repos_correct(self):
        backup_folder = BackupFolder("/home/user", "test")
        repos = backup_folder.get_relative_repo_paths()

        self.assertFalse(repos)


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
