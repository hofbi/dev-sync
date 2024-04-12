import subprocess
from pathlib import Path

from devsync.data import BackupFolder, Target
from devsync.sync import RSync


def test_get_options_with_dry_run() -> None:
    assert "-n" in RSync.get_options(True, [])


def test_get_options_without_dry_run() -> None:
    assert "-n" not in RSync.get_options(False, [])


def test_get_options_no_excludes() -> None:
    assert "--exclude" not in RSync.get_options(False, [])


def test_get_options_2_excludes() -> None:
    assert '--exclude="/tmp/foo"' in RSync.get_options(False, [Path("/tmp/foo"), Path("/tmp/bar")])
    assert '--exclude="/tmp/bar"' in RSync.get_options(False, [Path("/tmp/foo"), Path("/tmp/bar")])


def test_sync_no_excludes(monkeypatch) -> None:
    class MockCheckCall:
        def __init__(self):
            self.called = False
            self.call_args = None

        def __call__(self, *args, **kwargs):
            self.called = True
            self.call_args = (args, kwargs)

    mock_check_call = MockCheckCall()
    monkeypatch.setattr(subprocess, "check_call", mock_check_call)

    backup_folder = BackupFolder(Path("/foo"), "blub")
    backup_folder.get_relative_repo_paths = list

    rsync = RSync(Path("/foo"), [backup_folder])
    rsync.sync(Target("/tmp"), False)

    command = f"rsync {RSync.get_options(False, [])} {backup_folder.path} /tmp"
    assert mock_check_call.called
    assert mock_check_call.call_args == ((command,), {"shell": True, "cwd": Path("/foo")})


def test_sync_three_backup_folders(monkeypatch) -> None:
    class MockCheckCall:
        def __init__(self):
            self.call_count = 0

        def __call__(self, *args, **kwargs):
            self.call_count += 1

    mock_check_call = MockCheckCall()
    monkeypatch.setattr(subprocess, "check_call", mock_check_call)

    backup_folder = BackupFolder(Path("/foo"), "blub")
    backup_folder.get_relative_repo_paths = list

    rsync = RSync(Path("/foo"), [backup_folder, backup_folder, backup_folder])
    rsync.sync(Target("/tmp"), False)

    count_should_be = 3
    assert mock_check_call.call_count == count_should_be


def test_sync_no_backup(monkeypatch) -> None:
    class MockCheckCall:
        def __init__(self):
            self.called = False

        def __call__(self, *args, **kwargs):
            self.called = True

    mock_check_call = MockCheckCall()
    monkeypatch.setattr(subprocess, "check_call", mock_check_call)

    rsync = RSync(Path("/foo"), [])
    rsync.sync(Target("/tmp"), False)

    assert not mock_check_call.called
