import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        host="postgres",
        database="petdb",
        user="user",
        password="password"
    )

def save_to_db(input_text: str, output_text: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO processed_texts (input_text, output_text) VALUES (%s, %s)", (input_text, output_text))
    conn.commit()
    cur.close()
    conn.close()