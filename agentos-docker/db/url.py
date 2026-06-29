"""
Database URL
------------

Build database connection URL from environment variables.
"""

from os import getenv
from urllib.parse import quote


def build_db_url() -> str:
    """Build database URL from environment variables."""
    driver = getenv("DB_DRIVER", "postgresql+psycopg")
    user = getenv("DB_USER", "postgres")
    password = quote(getenv("DB_PASS", "postgres"), safe="")
    host = getenv("DB_HOST", "pgvector")
    port = getenv("DB_PORT", "5432")
    database = getenv("DB_DATABASE", "agentos_db")

    return f"{driver}://{user}:{password}@{host}:{port}/{database}"


db_url = build_db_url()
