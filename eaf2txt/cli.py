import argparse
from pathlib import Path

from .eaf2txt import convert_eaf_to_txt


def main():
    parser = argparse.ArgumentParser(prog='eaf2txt',
                                     description='Converts EAF files to tab-delimited txt files.')

    parser.add_argument('-f', '--file', metavar='eaf_file_path',
                        help='path to the EAF file.')
    parser.add_argument('-d', '--directory', metavar='directory_with_eaf_files',
                        help="path to a directory with EAF files.")
    parser.add_argument('--summary', action='store_const', const=True, default=False,
                        help="print a short summary after each conversion.")

    args = parser.parse_args()

    assert bool(args.file) ^ bool(args.directory), 'Exactly one of --file or --directory must be specified.'

    if args.file:
        path = Path(args.file)
        assert path.exists(), f'File {path} does not exist'
        assert path.is_file(), f'{path} is not a file'
        print(f'Converting {path}')
        convert_eaf_to_txt(path, summary=args.summary)

    if args.directory:
        path = Path(args.directory)
        assert path.exists(), f'Directory {path} does not exist'
        assert path.is_dir(), f'{path} is not a directory'
        for eaf_path in path.glob('*.eaf'):
            print(f'Converting {eaf_path}')
            convert_eaf_to_txt(eaf_path, summary=args.summary)


if __name__ == '__main__':
    main()
