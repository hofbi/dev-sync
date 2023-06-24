"""Test args module."""

from pathlib import Path

from pyfakefs.fake_filesystem_unittest import TestCase

from devsync.args import dir_path


class ArgsTest(TestCase):
    """Args test."""

    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_dir_path__is_dir__input_path(self):
        self.fs.create_dir("test")
        self.assertEqual(Path("test"), dir_path("test"))

    def test_dir_path__is_file__raise_not_a_directory_error(self):
        self.fs.create_file("test")
        with self.assertRaises(NotADirectoryError):
            dir_path("test")

    def test_dir_path__does_not_exist__raise_not_a_directory_error(self):
        with self.assertRaises(NotADirectoryError):
            dir_path("test")
