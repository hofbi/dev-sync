import os
import sys


NAME = 'Dev Sync'
VERSION = '1.0'
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
SHORT_DEST = os.path.join(SCRIPT_DIR, 'config', 'shortdest.yml')
LOGFILE = os.path.join(SCRIPT_DIR, 'logs', 'devsync.log')
