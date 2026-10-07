"""
A program that detects whether it is running
inside a Python virtual environment.
"""

import sys
import os
import site


def in_virtualenv() -> bool:
    """
    sys.prefix - points to the venv.
    sys.base_prefix - points to the global env.
    """
    has_real_prefix = hasattr(sys, "real_prefix")
    has_different_base = (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    return has_real_prefix or has_different_base


def get_venv_name(venv_path: str) -> str:
    """The folder name of the virtual env"""
    return os.path.basename(os.path.normpath(venv_path))


def get_site_packages_path() -> str | None:
    """Return the path to the site-packages dir currectly in use"""
    try:
        paths = site.getsitepackages()
        if paths:
            return paths[0]
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
    print("Current Python: {}".format(sys.executable))
    print("Virtual Environment: {}".format(venv_name))
    print("Environment path: {}".format(venv_path))
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print()
    print("Package installation path: {}".format(site_packages))


def print_outside() -> None:
    print()
    print("MATRIX STATUS: You're still plugged in")
    print()
    print("Current Python: {}".format(sys.executable))
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
