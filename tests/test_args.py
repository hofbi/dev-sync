"""Test args module."""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from devsync.args import dir_path, file_path


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


def test_file_path__is_dir__input_path(fs: FakeFilesystem) -> None:
    fs.create_file("test.txt")
    assert Path("test.txt") == file_path("test.txt")


def test_file_path__is_file__raise_file_not_found_error(fs: FakeFilesystem) -> None:
    fs.create_dir("test")
    with pytest.raises(FileNotFoundError):
        file_path("test")


def test_file_path__does_not_exist__raise_file_not_found_error() -> None:
    with pytest.raises(FileNotFoundError):
        file_path("test")
