import os
from typing import List

import tomllib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load app info from pyproject.toml
try:
    with open("pyproject.toml", "rb") as f:
        pyproject: dict = tomllib.load(f)
    APP_NAME: str = pyproject["project"]["name"]
    DESCRIPTION: str = pyproject["project"]["description"]
    VERSION: str = pyproject["project"]["version"]
except Exception:
    APP_NAME = "unknown"
    DESCRIPTION = ""
    VERSION = "unknown"

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

# Database settings - using standard PostgreSQL environment variables
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
# Database URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

# CORS Origins
ORIGINS: List[str] = os.getenv("ORIGINS", "http://localhost:8888").split(",")
