from pathlib import Path


def dir_path(path_string: str) -> Path:
    """
    Argparse type check if path is a directory
    :param path_string:
    :return:
    """
    if Path(path_string).is_dir():
        return Path(path_string)
    raise NotADirectoryError(path_string)
