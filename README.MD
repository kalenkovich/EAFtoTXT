# eaf2txt

A command-line utility to convert EAF files to tab-delimited txt files.
The output is written to a file with the same name but with '.txt' extension in the same directory as the source file.

## Installation

```sh
pip install git+https://github.com/kalenkovich/EAFtoTXT.git
```

## Usage

To convert a single file:

```sh
eaf2txt -f <path_to_file>
```

To convert all eaf files in a directory

```sh
eaf2txt -f <path_to_directory>
```

To save files to an sqlite database:

1. create the database with

    ```sh
    eaf2txt --create-database
    ```
   
2. add `--add-to-database` or `-add` argument when converting, e.g.:

    ```sh
    eaf2txt -f <path_to_file> -add
    ```
   
The database file will be looked for in the following locations (in this order):

1. File path supplied as the --path-to-database argument.
2. File path in the EAF2TXT_DB_PATH environment variable.
3. The eaf2txt.sqlite file in the current working directory.
