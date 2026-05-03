import argparse
import datetime

from dev_sync.args import dir_path, file_path
from dev_sync.config import NAME
from dev_sync.data import Target
from dev_sync.log import logger
from dev_sync.parser import YMLConfigParser
from dev_sync.sync import run_backup


def main():
    logger.info("%s\n", NAME)

    arguments = parse_arguments()
    config = arguments.config
    backup_target = Target(arguments.target)

    logger.info("Use config from: %s\n\n%s", config, config.read_text())
    logger.info("Starting Backup for %s\n", backup_target.path)
    yaml_parser = YMLConfigParser(config)
    run_backup(yaml_parser, backup_target, arguments.last_update, arguments.dry_run)

    logger.info("Finished Backup\n")


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
        type=file_path,
        help="Path to config file",
    )
    parser.add_argument(
        "--last_update",
        metavar=("YEAR", "MONTH", "DAY"),
        type=int,
        nargs=3,
        action=DateAction,
        default=(1970, 1, 1),
        help="Last time update was performed. This will just update repositories after this date. Format: YYYY MM DD",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making real changes",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
