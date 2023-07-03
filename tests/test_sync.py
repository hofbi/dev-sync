import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from pyfakefs.fake_filesystem_unittest import TestCase

from devsync.data import BackupFolder, Target
from devsync.sync import RepoSync, RSync


class RSyncTest(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_get_options_with_dry_run(self):
        self.assertIn("-n", RSync.get_options(True, []))

    def test_get_options_without_dry_run(self):
        self.assertNotIn("-n", RSync.get_options(False, []))

    def test_get_options_no_excludes(self):
        self.assertNotIn("--exclude", RSync.get_options(False, []))

    def test_get_options_2_excludes(self):
        self.assertIn(
            '--exclude="/tmp/foo"',
            RSync.get_options(False, [Path("/tmp/foo"), Path("/tmp/bar")]),
        )
        self.assertIn(
            '--exclude="/tmp/bar"',
            RSync.get_options(False, [Path("/tmp/foo"), Path("/tmp/bar")]),
        )

    @patch("devsync.sync.subprocess")
    def test_sync_no_excludes(self, mock_subprocess):
        backup_folder = BackupFolder(Path("/foo"), "blub")
        backup_folder.get_relative_repo_paths = MagicMock(return_value=[])
        rsync = RSync(Path("/foo"), [backup_folder])
        rsync.sync(Target("/tmp"), False)
        mock_subprocess.check_call.assert_called_with(
            f"rsync {RSync.get_options(False, [])} {backup_folder.path} {'/tmp'}".split(),
            cwd=Path("/foo"),
        )

    @patch("devsync.sync.subprocess")
    def test_sync_three_backup_folders(self, mock_subprocess):
        backup_folder = BackupFolder(Path("/foo"), "blub")
        backup_folder.get_relative_repo_paths = MagicMock(return_value=[])
        rsync = RSync(Path("/foo"), [backup_folder, backup_folder, backup_folder])
        rsync.sync(Target("/tmp"), False)
        self.assertEqual(3, mock_subprocess.check_call.call_count)

    @patch("devsync.sync.subprocess")
    def test_sync_no_backup(self, mock_subprocess):
        rsync = RSync(Path("/foo"), [])
        rsync.sync(Target("/tmp"), False)
        self.assertFalse(mock_subprocess.check_call.called)


class RepoSyncTest(unittest.TestCase):
    def test_get_all_repos_no_repos_set_empty(self):
        repo_sync = RepoSync(Path(), [])
        self.assertFalse(repo_sync.get_all_repos())
