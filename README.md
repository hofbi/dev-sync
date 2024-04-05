# Dev Sync

[![Actions Status](https://github.com/hofbi/dev-sync/workflows/CI/badge.svg)](https://github.com/hofbi/dev-sync)
[![Actions Status](https://github.com/hofbi/dev-sync/workflows/CodeQL/badge.svg)](https://github.com/hofbi/dev-sync)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a Python-based backup tool using [rsync](https://rsync.samba.org/) including backups for repositories based on [Git](https://git-scm.com/) and [Mercurial](https://www.mercurial-scm.org/).

## Usage

```shell
Dev Sync

usage: devsync.py [-h] [--last_update YEAR MONTH DAY] [--dry-run] target config

Backup Data and Repositories to external devices.

positional arguments:
  target                Destination path the where backup should be stored
  config                Path to config file

optional arguments:
  -h, --help            show this help message and exit
  --last_update YEAR MONTH DAY
                        Last time update was performed. This will just update repositories after this date.
                        Format: YYYY MM DD (default: (1970, 1, 1))
  --dry-run             Perform a dry run without making real changes (default: False)
```

## Config

The config file defines which folders should be saved. A sample config could look like below, which will backup all folders from `backupFolder` list relative to `home`

```shell
home: /home/user                    # Source root folder

backupFolder:                       # Folders that should be saved (relative to "home" variable)
  - path: Pictures                  # Folder name
  - path: Documents
  - path: Development
```

## Development

```shell
# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run coverage
make coverage
```
