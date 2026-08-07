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

        print("---")
        print(file.read())
        print("---")

        file.close()
        print(f"File '{filename}' closed.")

    except OSError as error:
        print(f"Error opening file '{filename}': {error}")


if __name__ == "__main__":
    main()
