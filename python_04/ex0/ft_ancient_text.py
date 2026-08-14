"""
Ancient Text Recovery

This program reads and displays the contents of a text file provided as a
command-line argument. It demonstrates basic file handling in Python.

Concepts:
- Command-line arguments: sys.argv is used to receive the filename from
  the user when the program is started.
- Type annotations: IO[str] indicates that the file object works with text
  data (strings).
- File handling: open() is used to open a file, read() retrieves its contents,
  and close() closes the file resource.
- Exception handling: try/except catches OSError if the file cannot be opened
  or another operating-system-related file error occurs.

Usage:
    python ft_ancient_text.py <file>

Example:
    python ft_ancient_text.py test_file
"""

import sys
from typing import IO


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    filename = sys.argv[1]

    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")

    try:
        file: IO[str] = open(filename, "r")

        print()
        print("---")
        print(file.read())
        print("---")
        print()

        file.close()
        print(f"File '{filename}' closed.")

    except OSError as error:
        print(f"Error opening file '{filename}': {error}")


if __name__ == "__main__":
    main()
