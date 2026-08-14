"""
Stream Management

This program reads text from a file given as a command-line argument,
displays the original content, transforms each line by adding a '#' character
to the end, and optionally saves the transformed content to a new file.

Concepts:
- Command-line arguments: sys.argv is used to receive the input filename.
- Standard input: sys.stdin.readline() reads the new filename from the user.
- Standard output: print() displays normal program messages on the screen.
- Standard error: print(..., file=sys.stderr) sends error messages to the
  standard error stream instead of normal output.
- File input: open() with "r" opens a file for reading, and read() retrieves
  its contents.
- File output: open() with "w" opens a file for writing, and write() saves
  the transformed data.
- Type annotations: IO[str] indicates that the file object handles text
  data represented by strings.
- String processing: splitlines() separates the file contents into lines.
- Loops: a for loop processes every line individually.
- String concatenation: += builds the transformed text one line at a time.
- Conditional statements: if/else determines whether the transformed data
  should be saved.
- Exception handling: try/except catches OSError when a file operation fails.
- Resource management: close() explicitly closes files after reading or
  writing.

Usage:
    python ft_stream_management.py <file>

The program demonstrates the difference between the three standard streams:
- stdin -> input received from the user
- stdout -> normal program output
- stderr -> error messages

Example:
    python ft_stream_management.py test_file
"""

import sys
from typing import IO


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management <file>")
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

        print("Enter new file name (or empty): ")
        new_filename = sys.stdin.readline().strip()

        if new_filename == "":
            print("Not saving data.")
        else:
            print(f"Saving data to '{new_filename}'")

            output: IO[str] = open(new_filename, "w")
            output.write(transformed)
            output.close()

            print(f"Data saved in file '{new_filename}'.")

    except OSError as error:
        print(
            f"[STDERR] Error opening file '{filename}': {error}",
            file=sys.stderr
        )


if __name__ == "__main__":
    main()
