import argparse
import datetime
from pathlib import Path

from devsync.args import dir_path
from devsync.config import NAME, VERSION
from devsync.data import Target
from devsync.log import logger
from devsync.parser import YMLConfigParser
from devsync.sync import run_backup


def main():
    logger.success(f"{NAME} {VERSION}\n")

    arguments = parse_arguments()
    config = Path(arguments.config.name)
    backup_target = Target(arguments.target)

    logger.verbose(f"Use config from: {config}\n\n{config.read_text()}")

    logger.notice(f"Starting Backup for {backup_target.path}\n")
    yaml_parser = YMLConfigParser(config)
    run_backup(yaml_parser, backup_target, arguments.last_update, arguments.dry_run)

    logger.success("Finished Backup\n")


def parse_arguments():
    class DateAction(argparse.Action):
        def __call__(self, arg_parser, args, values, option_string=None):
            last_update = datetime.datetime(
                year=int(values[0]),
                month=int(values[1]),
                day=int(values[2]),
                tzinfo=datetime.timezone.utc,
            ).timestamp()
            setattr(args, self.dest, last_update)

    parser = argparse.ArgumentParser(
        description="Backup Data and Repositories to external devices.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "target",
        type=dir_path,
        help="Destination path the where backup should be stored",
    )
    parser.add_argument(
        "config",
        type=argparse.FileType("r"),
        help="Path to config file",
    )
    parser.add_argument(
        "--last_update",
        metavar=("YEAR", "MONTH", "DAY"),
        type=int,
        nargs=3,
        action=DateAction,
        default=(1970, 1, 1),
        help="Last time update was performed. This will just update repositories after this date. "
        "Format: YYYY MM DD",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making real changes",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
