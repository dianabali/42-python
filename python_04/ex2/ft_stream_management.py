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
