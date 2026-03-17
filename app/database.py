"""
Модуль базы данных

Этот модуль обрабатывает операции с базой данных PostgreSQL для сохранения обработанных текстовых данных.
"""

import logging
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Установить соединение с базой данных PostgreSQL.

    Returns:
        psycopg2.connection: Объект соединения с базой данных.
    """
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="petdb",
            user="user",
            password="password"
        )
        logger.info("Соединение с базой данных установлено.")
        return conn
    except Exception as e:
        logger.error(f"Не удалось подключиться к базе данных: {str(e)}")
        raise

def save_to_db(input_text: str, output_text: str):
    """
    Сохранить входной и выходной текст в базу данных.

    Args:
        input_text (str): Исходный входной текст.
        output_text (str): Обработанный выходной текст.
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO processed_texts (input_text, output_text) VALUES (%s, %s)", (input_text, output_text))
        conn.commit()
        logger.info("Данные успешно сохранены в базу данных.")
    except Exception as e:
        logger.error(f"Не удалось сохранить данные в базу данных: {str(e)}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            cur.close()
            conn.close()
            logger.info("Соединение с базой данных закрыто.")