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
