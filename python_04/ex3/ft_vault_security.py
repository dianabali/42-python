"""
Vault Security

This program demonstrates how to safely read from and write to files using
a function called secure_archive().

The secure_archive() function accepts a filename, an action, and optional
content. It supports two operations:
- "read": opens a file and returns its contents.
- "write": creates or overwrites a file with the supplied content.

Instead of allowing file errors to crash the program, the function catches
OSError exceptions and returns a tuple containing a success status and a
message. This gives the caller a simple way to check whether the operation
was successful.

Concepts:
- File reading and writing: open() is used with "r" for reading and "w" for
  writing.
- Context managers: "with open(...)" automatically closes the file after the
  operation, even if an error occurs.
- Conditional statements: if/elif/else selects the requested file action
  and detects invalid actions.
- Exception handling: try/except catches OSError so file-related errors are
  returned instead of terminating the program.
- Tuples: the function returns (True, message) when successful and
  (False, message) when an operation fails.
- Boolean values: the first element of the returned tuple indicates whether
  the operation succeeded.
- Indexing: result[0] checks the success status and result[1] accesses the
  returned content or message.

The program tests the function with nonexistent, inaccessible, and regular
files. If reading the regular file succeeds, its contents are then written
to a new file.
"""


def secure_archive(
        filename: str,
        action: str = "read",
        content: str = ""
) -> tuple[bool, str]:

    try:
        if action == "read":
            with open(filename, "r") as file:
                return (True, file.read())
        elif action == "write":
            with open(filename, "w") as file:
                file.write(content)
            return (True, "Content successfully written to file")
        else:
            return (False, "Invalid action")
    except OSError as error:
        return (False, str(error))


def main() -> None:
    print("=== Cyber Archives Security ===")

    print()

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))

    print()

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("no_permissions"))

    print()

    print("Using 'secure_archive' to read from a regular file:")
    result = secure_archive("test")
    print(result)
    print()

    if result[0]:
        print(
            "Using 'secure_archive' to write previous content to a new file:"
        )
        print(
            secure_archive(
                "write_test",
                "write",
                result[1]
            )
        )


if __name__ == "__main__":
    main()
