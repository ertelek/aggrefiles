# aggrefiles

`aggrefiles` is a simple command-line tool that scans a folder (and its
subfolders), finds all files with a specific extension, and aggregates
them into a single output file.

You can also provide a `.gitignore` file so ignored files and folders
are skipped automatically.

## Features

-   Recursively collects files with a chosen extension
-   Writes each file's **relative path**, then its **contents**, then a
    separator line
-   Supports `.gitignore` patterns using `pathspec`
-   Easy to run as a CLI tool

## Installation

From inside the project folder (after setting up your virtual
environment):

``` bash
python -m venv .env
source .env/bin/activate
pip install .
```

This installs the `aggrefiles` command on your system/venv.

## Usage

### Basic use

Aggregate all `.txt` files under the current directory:

``` bash
aggrefiles
```

### Choose a directory and extension

``` bash
aggrefiles src --ext .py
```

### Specify an output file

``` bash
aggrefiles . --ext .log --output logs_combined.txt
```

### Use a `.gitignore` file

``` bash
aggrefiles . --ext .py --gitignore .gitignore
```

Files or folders matching the patterns in the gitignore file will be
skipped.

## Output Format

For each matched file, the output file will contain:

    relative/path/to/file1.ext
    <file1 contents>
    ------------------------------
    relative/path/to/file2.ext
    <file2 contents>
    ------------------------------

## Requirements

-   Python 3.8+
-   `pathspec` (installed automatically when installing the package)

## Contributing

Contributions are welcome!  
If you’d like to add features, improve UX, or fix bugs, open an issue or pull request in the project repository.

## License

MIT License — © 2025 Értelek
