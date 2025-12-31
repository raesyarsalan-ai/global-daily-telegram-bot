import sqlite3

DB_NAME = "bot.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        language TEXT DEFAULT 'en'
    )
    """)

    conn.commit()
    conn.close()


def get_language(user_id: int) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT language FROM users WHERE user_id = ?",
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else "en"


def set_language(user_id: int, language: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (user_id, language)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET language = excluded.language
    """, (user_id, language))

    conn.commit()
    conn.close()
