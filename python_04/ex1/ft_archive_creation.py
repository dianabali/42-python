"""
Archive Creation

This program reads the contents of a text file, displays the original data,
transforms each line by adding a '#' character to the end, and optionally
saves the transformed data into a new file.

Concepts:
- Command-line arguments: sys.argv is used to get the input filename from
  the command line.
- Type annotations: IO[str] indicates that the file object is used to read
  and write text (strings).
- File reading: open() opens the input file and read() retrieves its contents.
- String processing: splitlines() separates the text into individual lines.
- Loops: a for loop processes each line and adds '#' to it.
- String concatenation: += is used to build the transformed text.
- User input: input() allows the user to choose whether to save the result.
- File writing: open() with "w" creates or overwrites a file, and write()
  stores the transformed data.
- Conditional statements: if/else determines whether the transformed data
  should be saved.
- Exception handling: try/except catches OSError when a file cannot be
  opened, read, or written.

Usage:
    python ft_archive_creation.py <file>

Example:
    python ft_archive_creation.py test_file
"""

import sys
from typing import IO


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    filename = sys.argv[1]

    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    try:
        file: IO[str] = open(filename, "r")
        content = file.read()

        print("---")
        print()
        print(content)
        print()
        print("---")

        file.close()
        print(f"File '{filename}' closed.")

        print()
        print("Transform data:")

        transformed = ""
        for line in content.splitlines():
            transformed += line + "#\n"

        print("---")
        print()
        print(transformed)
        print("---")

        new_filename = input("Enter new file name (or empty): ")

        if new_filename == "":
            print("Not saving data.")
        else:
            print(f"Saving data to '{new_filename}'")

            output: IO[str] = open(new_filename, "w")
            output.write(transformed)
            output.close()

            print(f"Data saved in file '{new_filename}'.")
    except OSError as error:
        print(f"Error opening file '{filename}': {error}")


if __name__ == "__main__":
    main()
