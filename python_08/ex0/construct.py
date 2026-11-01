import sys
import os
import site 
# site - to find the site-packages
# site-packages - a dir where Python stores installed 
# 3rd party libraries / packages


def in_virtualenv() -> bool:
    """
    sys.prefix - the current active env
    sys.base_prefix - the global env

    Same - global
    Different - virtual
    """

    return sys.prefix != sys.base_prefix


def get_venv_name(venv_path: str) -> str:
    """The folder name of the virtual env"""
    return os.path.basename(os.path.normpath(venv_path))


def get_site_packages_path() -> str | None:
    """Return the path to the site-packages dir in use"""
    try:
        pathh = site.getsitepackages()
        if pathh:
            return pathh[0]
    except Exception as error:
        print(f"Error accessing the virtual environment: {error}")
    return None


def print_inside() -> None:
    venv_path = sys.prefix
    venv_name = get_venv_name(venv_path)
    site_packages = get_site_packages_path()
    print()

    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment path: {venv_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print()
    print(f"Package installation path: {site_packages}")


def print_outside() -> None:
    print()
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate   # On Unix")
    print("matrix_env\\Scripts\\activate    # On Windows")
    print()
    print("Then run this program again.")


def main() -> None:
    if in_virtualenv():
        print_inside()
    else:
        print_outside()


if __name__ == "__main__":
    main()
