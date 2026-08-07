def secure_archive(filename, action="read", content=""):
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


def main():
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

    if result[0]:
        print(
            "Using 'secure_archive' to write previous content to a new file:"
        )
        print(
            secure_archive(
                "test1",
                "write",
                result[1]
            )
        )


if __name__ == "__main__":
    main()
