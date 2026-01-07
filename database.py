import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
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
        is_premium BOOLEAN DEFAULT FALSE,
        premium_until TIMESTAMP,
        ai_requests INT DEFAULT 0,
        device_hash TEXT,
        blocked BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ai_memory (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT,
        role TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT,
        invoice_id TEXT UNIQUE,
        amount NUMERIC,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# =========================
# USER SECURITY
# =========================
def lock_device(telegram_id, device_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users SET device_hash=%s
        WHERE telegram_id=%s AND device_hash IS NULL
    """, (device_hash, telegram_id))
    conn.commit()
    cur.close()
    conn.close()


def check_device(telegram_id, device_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT device_hash FROM users WHERE telegram_id=%s
    """, (telegram_id,))
    u = cur.fetchone()
    cur.close()
    conn.close()

    if not u:
        return True
    if u["device_hash"] is None:
        return True
    return u["device_hash"] == device_hash


# =========================
# PREMIUM
# =========================
def activate_premium(telegram_id, days=30):
    until = datetime.utcnow() + timedelta(days=days)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET is_premium=TRUE, premium_until=%s
        WHERE telegram_id=%s
    """, (until, telegram_id))
    conn.commit()
    cur.close()
    conn.close()


def is_premium(telegram_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT is_premium, premium_until
        FROM users WHERE telegram_id=%s
    """, (telegram_id,))
    u = cur.fetchone()
    cur.close()
    conn.close()

    if not u or not u["is_premium"]:
        return False
    if u["premium_until"] < datetime.utcnow():
        return False
    return True
