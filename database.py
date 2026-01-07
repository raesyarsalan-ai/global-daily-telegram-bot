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
        last_device TEXT,
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
        order_id TEXT UNIQUE,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# =========================
# PREMIUM
# =========================
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
    if u["premium_until"] and u["premium_until"] < datetime.utcnow():
        return False
    return True


# =========================
# AI MEMORY
# =========================
def save_ai_message(telegram_id, role, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ai_memory (telegram_id, role, content)
        VALUES (%s, %s, %s)
    """, (telegram_id, role, content))
    conn.commit()
    cur.close()
    conn.close()


def get_ai_context(telegram_id, limit=6):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT role, content FROM ai_memory
        WHERE telegram_id=%s
        ORDER BY created_at DESC
        LIMIT %s
    """, (telegram_id, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return list(reversed(rows))


# =========================
# RATE LIMIT
# =========================
def increase_ai_usage(telegram_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET ai_requests = ai_requests + 1
        WHERE telegram_id=%s
    """, (telegram_id,))
    conn.commit()
    cur.close()
    conn.close()
