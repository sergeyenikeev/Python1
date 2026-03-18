"""Database helpers for storing processed texts."""

import logging
import os

import psycopg2

logger = logging.getLogger(__name__)

DEFAULT_DATABASE_URL = "postgresql://user:password@postgres:5432/petdb"


def get_database_url() -> str:
    """Return the configured database DSN."""
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_db_connection():
    """Create a PostgreSQL connection."""
    try:
        conn = psycopg2.connect(get_database_url())
        logger.info("Database connection established.")
        return conn
    except Exception:
        logger.exception("Failed to connect to PostgreSQL.")
        raise


def save_to_db(input_text: str, output_text: str) -> None:
    """Persist the original and processed text."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO processed_texts (input_text, output_text) VALUES (%s, %s)",
            (input_text, output_text),
        )
        conn.commit()
        logger.info("Processed text saved to the database.")
    except Exception:
        logger.exception("Failed to save processed text to the database.")
        if conn:
            conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            logger.info("Database connection closed.")
