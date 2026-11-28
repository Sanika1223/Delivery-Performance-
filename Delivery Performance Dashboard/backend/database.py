
import os
from pathlib import Path

import psycopg2


# Load variables from the backend/.env file
ENV_FILE = Path(__file__).resolve().parent / ".env"

if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()

        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), value)


# Get the Neon database connection string
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is missing. Please check backend/.env"
        )

    connection = psycopg2.connect(DATABASE_URL)
    return connection
