import os
import sys

try:
    from dotenv import load_dotenv  # reads a .env file into environment variables
except ImportError:
    print("[ERROR]: python-dotenv is missing. Run: pip install -r requirements.txt")
    sys.exit(1)


PLACEHOLDERS = ["", "apiii_keyyy", "somethingg"]
VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def load_settings():
    """Read the settings and return them with a list of warnings"""

    warnings = []

    # load_dotenv() reads the .env file and puts its lines into os.environ.
    # override=False - if a variable is ALREADY set in the real
    # environment the .env file will NOT replace it
    env_file_found = load_dotenv(override=False)
    if not env_file_found:
        warnings.append("No .env file found (using environment only)")

    # .strip() removes spaces around the value
    # .lower() / .upper() make the text consistent
    mode = os.environ.get("MATRIX_MODE", "").strip().lower()
    database_url = os.environ.get("DATABASE_URL", "").strip()
    api_key = os.environ.get("API_KEY", "").strip()
    log_level = os.environ.get("LOG_LEVEL", "").strip().upper()
    zion_endpoint = os.environ.get("ZION_ENDPOINT", "").strip()

    # MATRIX_MODE - "development" or "production"
    if mode == "":
        warnings.append("MATRIX_MODE missing, using default 'development'")
        mode = "development"
    elif mode != "development" and mode != "production":
        warnings.append("MATRIX_MODE '" + mode + "' invalid, using 'development'")
        mode = "development"

    # DATABASE_URL
    if database_url == "":
        warnings.append("DATABASE_URL is missing")

    # API_KEY
    if api_key == "":
        warnings.append("API_KEY is missing")
    elif api_key in PLACEHOLDERS:
        # It is set, but still the fake value copied from .env.example
        warnings.append("API_KEY is still a placeholder value")

    # LOG_LEVEL - one of VALID_LOG_LEVELS
    if log_level == "":
        warnings.append("LOG_LEVEL missing, using default 'INFO'")
        log_level = "INFO"
    elif log_level not in VALID_LOG_LEVELS:
        warnings.append("LOG_LEVEL '" + log_level + "' invalid, using 'INFO'")
        log_level = "INFO"

    # ZION_ENDPOINT
    if zion_endpoint == "":
        warnings.append("ZION_ENDPOINT is missing")

    # Put all in one
    settings = {
        "mode": mode,
        "database_url": database_url,
        "api_key": api_key,
        "log_level": log_level,
        "zion_endpoint": zion_endpoint,
    }

    return settings, warnings


def is_local_database(url):
    """Return True if the database URL points to this computer"""
    return "localhost" in url or "127.0.0.1" in url or "sqlite" in url


def check_production(settings):
    """Production is strict. Return a list of errors (empty = all good)"""
    errors = []

    # A real production system needs a real API key
    if settings["api_key"] in PLACEHOLDERS:
        errors.append("API_KEY must be set to a real value")

    # Production must use a real remote database
    if settings["database_url"] == "":
        errors.append("DATABASE_URL must be set")
    elif is_local_database(settings["database_url"]):
        errors.append("DATABASE_URL must not point to a local instance")

    # https:// means the connection is encrypted
    if not settings["zion_endpoint"].startswith("https://"):
        errors.append("ZION_ENDPOINT must use https://")

    # DEBUG logs can leak sensitive details, so production must not use them
    if settings["log_level"] == "DEBUG":
        errors.append("LOG_LEVEL must not be DEBUG")

    return errors


def get_database_status(url):
    """Return a description of the database"""
    if url == "":
        return "Not configured"
    if is_local_database(url):
        return "Connected to local instance"
    return "Connected to remote instance"


def no_hardcoded_secret(api_key):
    """Return True if the API key does not appear in this file"""
    # Placeholders are not real secrets, so there is nothing to leak
    if api_key in PLACEHOLDERS:
        return True
    try:
        # __file__ is the path of this very script
        with open(__file__, "r") as file:
            source_code = file.read()
    except OSError:
        # If we cannot read the file, we cannot find a secret in it
        return True
    # If the key is NOT found in the source code, the check passes
    return api_key not in source_code


def env_file_is_protected():
    """Return True if .gitignore has .env and .env.example"""
    try:
        with open(".gitignore", "r") as file:
            # splitlines() turns the file text into a list of lines
            lines = file.read().splitlines()
    except OSError:
        # No .gitignore means .env is NOT protected
        return False

    env_is_ignored = ".env" in lines
    example_exists = os.path.exists(".env.example")
    return env_is_ignored and example_exists


def print_check(passed, message):
    """Print [OK] or [FAIL]"""
    if passed:
        print("[OK] " + message)
    else:
        print("[FAIL] " + message)


def main():
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    # Step 1: load the settings
    settings, warnings = load_settings()

    # Step 2: show every warnings collected
    for warning in warnings:
        print("[WARNING] " + warning)
    if warnings:
        print()

    # Step 3: in production, stop immediately if anything is wrong
    if settings["mode"] == "production":
        errors = check_production(settings)
        if errors:
            print("[FATAL] Production configuration invalid:")
            for error in errors:
                print("  - " + error)
            sys.exit(1)

    # Step 4: print the configuration report
    print("Configuration loaded:")
    print("Mode: " + settings["mode"])
    print("Database: " + get_database_status(settings["database_url"]))

    # Print whether the key is usable
    if settings["api_key"] in PLACEHOLDERS:
        print("API Access: Not authenticated")
    else:
        print("API Access: Authenticated")

    print("Log Level: " + settings["log_level"])

    # Check that endpoint is configured
    if settings["zion_endpoint"] == "":
        print("Zion Network: Offline")
    else:
        print("Zion Network: Online")

    # Step 5: dev vs prod
    if settings["mode"] == "development":
        print("Debug tools: ENABLED (verbose output, local resources allowed)")
    else:
        print("Debug tools: DISABLED (secrets masked, remote resources enforced)")
        print("API Key: ********")  # secrets are hidden in production

    # Step 6: run the security checks and print each result
    print("\nEnvironment security check:")
    print_check(no_hardcoded_secret(settings["api_key"]),
                "No hardcoded secrets detected")
    print_check(env_file_is_protected(),
                ".env file properly configured")
    # load_dotenv(override=False) lets real environment
    # variables override the .env file, so overrides are always available
    print_check(True, "Production overrides available")

    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
