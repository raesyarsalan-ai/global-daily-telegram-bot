import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def get_connection():
    """Create a new PostgreSQL connection."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

def init_db():
    """Initialize all required tables in the database."""
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        language VARCHAR(10) DEFAULT 'en',
        is_premium BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

# User utility methods

def get_user_by_telegram_id(telegram_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def create_user(telegram_id, username, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, username, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (telegram_id, username, password_hash))
    conn.commit()
    cur.close()
    conn.close()
    return True

def set_user_language(telegram_id, language):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users SET language = %s WHERE telegram_id = %s;
    """, (language, telegram_id))
    conn.commit()
    cur.close()
    conn.close()

def get_user_language(telegram_id):
    user = get_user_by_telegram_id(telegram_id)
    if user and "language" in user:
        return user["language"]
    return "en"
