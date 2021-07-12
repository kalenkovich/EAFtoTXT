# eaf2txt

A command-line utility to convert EAF files to tab-delimited txt files.
The output is written to a file with the same name but with '.txt' extension in the same directory as the source file.

To convert a single file:

```sh
python -m eaf2txt.cli -f <path_to_file>
```

To convert all eaf files in a directory

```sh
python -m eaf2txt.cli -f <path_to_directory>
```

The utility has to be run from the repository root.
