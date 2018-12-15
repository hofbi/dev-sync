# Dev Sync

[![Build Status](https://travis-ci.org/hofbi/dev-sync.svg?branch=master)](https://travis-ci.org/hofbi/dev-sync)

This is my python backup tool based on [rsync](https://rsync.samba.org/) including backups for all my repositories ([Git](https://git-scm.com/) and [Mercurial](https://www.mercurial-scm.org/))

## Usage

```shell
Dev Sync 1.0

usage: devsync.py [-h] [--last_update YEAR MONTH DAY] [--dry-run]
                  DESTINATION CONFIG_FILE

Backup Data and Repositories to external devices.

positional arguments:
  DESTINATION           Destination path where backup should be stored -->
                        Also accepts destination shortcuts defined in
                        res/shortdest.yml
  CONFIG_FILE           Path to config file

optional arguments:
  -h, --help            show this help message and exit
  --last_update YEAR MONTH DAY
                        Last time update was performed. This will just update
                        repositories after this date. Format: YYYY MM DD
                        (default: (1970, 1, 1))
  --dry-run             Perform a dry run without making real changes
                        (default: False)
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

For often used backup destinations there is also a `shortdest.yml` which contains shortcuts for these paths. This shortcut name can also be passed as argument for `DESTINATION`.

```shell
shortDests:                         # Destination Shortcuts
  - shortDest: TEST                 # Destination name (selectable by CLI argument)
    destPath: /tmp/                 # Root path of destination
  - shortDest: USB
    destPath: /media/user/usbdevice
```