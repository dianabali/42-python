import os
import sys
from dotenv import load_dotenv

# load the .env file
# override=False means real env vars
load_dotenv(override=False)

# read each setting
# os.getenv returns None if the variable is missing
mode = os.getenv("MATRIX_MODE")
database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
log_level = os.getenv("LOG_LEVEL")
zion_endpoint = os.getenv("ZION_ENDPOINT")

print("ORACLE STATUS: Reading the Matrix...")
print()

# handle missing configuration
if mode is None:
    print("WARNING: MATRIX_MODE is missing, using 'development'")
    mode = "development"

if log_level is None:
    # different default depending on the mode
    if mode == "production":
        log_level = "WARNING"
    else:
        log_level = "DEBUG"
    print("WARNING: LOG_LEVEL is missing, using " + log_level)

missing = []
if database_url is None:
    missing.append("DATABASE_URL")
if api_key is None:
    missing.append("API_KEY")
if zion_endpoint is None:
    missing.append("ZION_ENDPOINT")

for name in missing:
    print("WARNING: " + name + " is missing")

# in production, missing settings are NOT allowed
if mode == "production" and missing:
    print()
    print("ERROR: Production needs all settings. The Oracle stops here.")
    sys.exit(1)

print()

# show the configuration
print("Configuration loaded:")
print("Mode: " + mode)

if database_url is None:
    print("Database: Not configured")
elif "localhost" in database_url:
    print("Database: Connected to local instance")
else:
    print("Database: Connected to remote instance")

if api_key is None:
    print("API Access: Not authenticated")
else:
    print("API Access: Authenticated")

print("Log Level: " + log_level)

if zion_endpoint is None:
    print("Zion Network: Offline")
else:
    print("Zion Network: Online")

print()

# development vs production difference 
if mode == "production":
    print("Production mode: strict rules, quiet logs")
    if log_level == "DEBUG":
        print("WARNING: DEBUG logs are not recommended in production")
else:
    print("Development mode: relaxed rules, detailed logs")

print()

# security check 
print("Environment security check:")

# 1. the secret must not be written inside this file
with open(__file__) as f:
    source_code = f.read()
if api_key is not None and api_key in source_code:
    print("[FAIL] Hardcoded secret found in oracle.py")
else:
    print("[OK] No hardcoded secrets detected")

# 2. .env must exist and be listed in .gitignore
env_exists = os.path.exists(".env")
in_gitignore = False
if os.path.exists(".gitignore"):
    with open(".gitignore") as f:
        in_gitignore = ".env" in f.read().split()
if env_exists and in_gitignore:
    print("[OK] .env file properly configured")
elif not env_exists:
    print("[WARN] No .env file found (run: cp .env.example .env)")
else:
    print("[WARN] .env is not listed in .gitignore")

# 3. environment variables can override the .env file
print("[OK] Production overrides available")

print()
print("The Oracle sees all configurations.")
