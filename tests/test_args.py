"""Test args module."""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from devsync.args import dir_path


def test_dir_path__is_dir__input_path(fs: FakeFilesystem) -> None:
    fs.create_dir("test")
    assert Path("test") == dir_path("test")


def test_dir_path__is_file__raise_not_a_directory_error(fs: FakeFilesystem) -> None:
    fs.create_file("test")
    with pytest.raises(NotADirectoryError):
        dir_path("test")


def test_dir_path__does_not_exist__raise_not_a_directory_error() -> None:
    with pytest.raises(NotADirectoryError):
        dir_path("foo")
