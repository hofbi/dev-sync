from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem

from devsync.log import init_logging


def test_init_logging___logfile_path_does_not_exist__should_be_created(
    fs: FakeFilesystem,
) -> None:
    init_logging(Path("logs/logfile"))
    assert fs.exists("logs/logfile")
