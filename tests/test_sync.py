from pathlib import Path

from devsync.data import BackupFolder, Target
from devsync.sync import RepoSync, RSync


def test_get_options_with_dry_run() -> None:
    assert "-n" in RSync.get_options(True, [])


def test_get_options_without_dry_run() -> None:
    assert "-n" not in RSync.get_options(False, [])


def test_get_options_no_excludes() -> None:
    assert "--exclude" not in RSync.get_options(False, [])


def test_get_options_2_excludes() -> None:
    assert '--exclude="/tmp/foo"' in RSync.get_options(False, [Path("/tmp/foo"), Path("/tmp/bar")])
    assert '--exclude="/tmp/bar"' in RSync.get_options(False, [Path("/tmp/foo"), Path("/tmp/bar")])


def test_sync_no_excludes(fake_process) -> None:
    backup_folder = BackupFolder(Path("/foo"), "blub")
    backup_folder.get_relative_repo_paths = list

    command = f"rsync {RSync.get_options(False, [])} {backup_folder.path} /tmp"

    fake_process.register(command)
    rsync = RSync(Path("/foo"), [backup_folder])
    rsync.sync(Target("/tmp"), False)
    assert fake_process.call_count(f"rsync {RSync.get_options(False, [])} {backup_folder.path} /tmp") == 1


def test_sync_three_backup_folders(fake_process):
    backup_folder = BackupFolder(Path("/foo"), "blub")
    backup_folder.get_relative_repo_paths = list

    command = f"rsync {RSync.get_options(False, [])} {backup_folder.path} /tmp"

    fake_process.register(command, occurrences=3)

    rsync = RSync(Path("/foo"), [backup_folder, backup_folder, backup_folder])
    rsync.sync(Target("/tmp"), False)

    expected_count = 3
    assert fake_process.call_count(command) == expected_count


def test_sync_no_backup(fake_process) -> None:
    rsync = RSync(Path("/foo"), [])
    rsync.sync(Target("/tmp"), False)
    assert not fake_process.calls


def test_get_all_repos_no_repos_set_empty() -> None:
    repo_sync = RepoSync(Path(), [])
    assert not repo_sync.get_all_repos()
