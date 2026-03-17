"""
Database Module

This module handles PostgreSQL database operations for saving processed text data.
"""

import logging
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database.

    Returns:
        psycopg2.connection: The database connection object.
    """
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="petdb",
            user="user",
            password="password"
        )
        logger.info("Database connection established.")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

def save_to_db(input_text: str, output_text: str):
    """
    Save the input and output text to the database.

    Args:
        input_text (str): The original input text.
        output_text (str): The processed output text.
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO processed_texts (input_text, output_text) VALUES (%s, %s)", (input_text, output_text))
        conn.commit()
        logger.info("Data saved to database successfully.")
    except Exception as e:
        logger.error(f"Failed to save data to database: {str(e)}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            cur.close()
            conn.close()
            logger.info("Database connection closed.")