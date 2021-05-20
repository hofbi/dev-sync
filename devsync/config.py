from pathlib import Path


NAME = "Dev Sync"
VERSION = "1.0"
SCRIPT_DIR = Path(__file__).absolute().parent.parent
SHORT_DEST = SCRIPT_DIR / "config" / "shortdest.yml"
LOGFILE = SCRIPT_DIR / "logs" / "devsync.log"
