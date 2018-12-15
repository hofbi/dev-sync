import argparse
import datetime

from devsync.log import logger
from devsync.parser import YMLConfigParser
from devsync.sync import run_backup
from devsync.config import NAME, VERSION, SCRIPT_DIR, SHORT_DEST


def main():
    logger.success('{} {}\n'.format(NAME, VERSION))

    # Parsing Arguments
    args = parse_arguments()
    config = args.config.name
    backup_target = YMLConfigParser.get_target_from_argument(SHORT_DEST, args.target[0])
    report = args.dry_run
    last_update = args.last_update

    print_selected_config(config)

    logger.notice('Starting Backup for {}\n'.format(backup_target.path))
    yaml_parser = YMLConfigParser(config)
    run_backup(yaml_parser, backup_target, last_update, report)

    logger.success('Finished Backup\n')


def parse_arguments():
    class DateAction(argparse.Action):
        def __call__(self, arg_parser, args, values, option_string=None):
            last_update = datetime.datetime(year=values[0], month=values[1], day=values[2],
                                            tzinfo=datetime.timezone.utc).timestamp()
            setattr(args, self.dest, last_update)

    parser = argparse.ArgumentParser(description='Backup Data and Repositories to external devices.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('target', metavar='DESTINATION', type=str, nargs=1,
                        help='Destination path where backup should be stored --> Also accepts destination shortcuts '
                             'defined in ' + SHORT_DEST.replace(SCRIPT_DIR + '/', ''))
    parser.add_argument('config', metavar='CONFIG_FILE', type=argparse.FileType('r'),
                        help='Path to config file')
    parser.add_argument('--last_update', metavar=('YEAR', 'MONTH', 'DAY'), type=int, nargs=3, action=DateAction,
                        default=(1970, 1, 1),
                        help='Last time update was performed. This will just update repositories after this date. '
                             'Format: YYYY MM DD')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='Perform a dry run without making real changes')

    return parser.parse_args()


def print_selected_config(config_path):
    with open(config_path, 'r') as fin:
        logger.verbose('Use config from: {}\n\n{}'.format(config_path.replace(SCRIPT_DIR + '/', ''), fin.read()))


if __name__ == '__main__':
    main()
