"""
Unit tests for database operations.
"""

import pytest
from unittest.mock import patch, MagicMock
from app.database import get_db_connection, save_to_db

@patch('app.database.psycopg2.connect')
def test_get_db_connection(mock_connect):
    """Test database connection."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    conn = get_db_connection()
    assert conn == mock_conn
    mock_connect.assert_called_once()

@patch('app.database.get_db_connection')
def test_save_to_db(mock_get_conn):
    """Test saving data to database."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_get_conn.return_value = mock_conn

    save_to_db("input", "output")

    mock_cur.execute.assert_called_once_with(
        "INSERT INTO processed_texts (input_text, output_text) VALUES (%s, %s)",
        ("input", "output")
    )
    mock_conn.commit.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()