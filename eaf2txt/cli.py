import argparse
import os
from pathlib import Path

from .eaf2txt import convert_eaf_to_txt
from .db import create_database


DB_PATH_ENV_VAR = 'EAF2TXT_DB_PATH'
DB_FILENAME = 'eaf2txt.sqlite'


def _get_database_path(args_database_path):
    db_path = args_database_path or os.environ.get(DB_PATH_ENV_VAR) or (Path(os.getcwd()) / DB_FILENAME)
    if not db_path.exists():
        raise FileNotFoundError(f'There is no database file at {db_path}.\n'
                                f'Path to the database can be set as the --database-path argument or the '
                                f'{DB_PATH_ENV_VAR} environment variable.\n'
                                f'Otherwise, we look for {DB_FILENAME} file in the current working directory.\n',
                                f'\n'
                                f'If you haven\'t yet created the database file, you can do so with '
                                f'--create-database argument.')


def main():
    parser = argparse.ArgumentParser(prog='eaf2txt',
                                     description='Converts EAF files to tab-delimited txt files.')

    parser.add_argument('-f', '--file', metavar='eaf_file_path',
                        help='path to the EAF file.')
    parser.add_argument('-d', '--directory', metavar='directory_with_eaf_files',
                        help="path to a directory with EAF files.")
    parser.add_argument('--summary', action='store_const', const=True, default=False,
                        help="print a short summary after each conversion.")

    # database-related arguments
    parser.add_argument('-add', '--add-to-database', action='store_const', const=True, default=False,
                        help="add to database in addition to conversion.")
    parser.add_argument('--database-path', metavar='database_file_path',
                        help="path to the database file.")
    parser.add_argument('--create-database', action='store_const', const=True, default=False,
                        help=f"create an empty database at --database-path, {DB_PATH_ENV_VAR}, or current working "
                             "directory.")

    args = parser.parse_args()

    if args.create_database:
        db_path = args.database_path or os.environ.get(DB_PATH_ENV_VAR)
        if not db_path:
            db_path = Path(os.getcwd()) / DB_FILENAME
            print(f'Neither the --database-path argument nor the environment variable {DB_PATH_ENV_VAR} are present. '
                  f'The database will be created at {db_path}. Print yes to proceed, anything else to cancel.')
            answer = input()
            if answer != 'yes':
                return

        print(f'Creating an empty database at {db_path}')
        create_database(Path(db_path))
        return

    assert bool(args.file) ^ bool(args.directory), 'Exactly one of --file or --directory must be specified.'

    if args.file:
        path = Path(args.file)
        assert path.exists(), f'File {path} does not exist'
        assert path.is_file(), f'{path} is not a file'
        eaf_paths = [path]

    if args.directory:
        path = Path(args.directory)
        assert path.exists(), f'Directory {path} does not exist'
        assert path.is_dir(), f'{path} is not a directory'
        eaf_paths = path.glob('*.eaf')

    if args.add_to_database:
        db_path = _get_database_path(args.database_path)
    else:
        db_path = None

    for eaf_path in eaf_paths:
        print(f'Converting {eaf_path}')
        convert_eaf_to_txt(eaf_path, summary=args.summary, path_to_database=db_path)


if __name__ == '__main__':
    main()
