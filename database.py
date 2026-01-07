import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE NOT NULL,
        language VARCHAR(5) DEFAULT 'en',
        device_fingerprint TEXT,
        is_premium BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rate_limits (
        telegram_id BIGINT PRIMARY KEY,
        count INT DEFAULT 0,
        reset_at TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_user(telegram_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id=%s", (telegram_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def create_user(telegram_id, language, device_fp):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, language, device_fingerprint)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id) DO NOTHING
    """, (telegram_id, language, device_fp))
    conn.commit()
    cur.close()
    conn.close()


def update_device(telegram_id, device_fp):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users SET device_fingerprint=%s
        WHERE telegram_id=%s
    """, (device_fp, telegram_id))
    conn.commit()
    cur.close()
    conn.close()
