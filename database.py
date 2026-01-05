import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE NOT NULL,
        username TEXT,
        language VARCHAR(10) DEFAULT 'en',
        is_premium BOOLEAN DEFAULT FALSE,
        session_id TEXT,
        last_login TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # shopping
    cur.execute("""
    CREATE TABLE IF NOT EXISTS shopping (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        items TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        remind_at TEXT
    );
    """)

    # tasks
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        text TEXT NOT NULL,
        done BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


# ---------- SESSION MANAGEMENT ----------

def save_session(telegram_id: int, session_id: str, username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, username, session_id, last_login)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (telegram_id)
        DO UPDATE SET
            session_id = EXCLUDED.session_id,
            last_login = EXCLUDED.last_login,
            username = EXCLUDED.username;
    """, (telegram_id, username, session_id, datetim
