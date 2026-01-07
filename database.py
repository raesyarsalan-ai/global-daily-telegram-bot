import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# =========================
# CONNECTION
# =========================
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )


# =========================
# INIT DB
# =========================
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE NOT NULL,
        username TEXT,
        is_premium BOOLEAN DEFAULT FALSE,
        premium_until TIMESTAMP,
        language TEXT DEFAULT 'en',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL,
        order_id TEXT UNIQUE NOT NULL,
        amount_usd NUMERIC NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT,
        text TEXT,
        remind_at TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# =========================
# USERS
# =========================
def get_or_create_user(telegram_id, username=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE telegram_id=%s", (telegram_id,))
    user = cur.fetchone()

    if not user:
        cur.execute("""
            INSERT INTO users (telegram_id, username)
            VALUES (%s, %s)
            RETURNING *
        """, (telegram_id, username))
        user = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()
    return user


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
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or not user["is_premium"]:
        return False
    if user["premium_until"] and user["premium_until"] < datetime.utcnow():
        return False
    return True


# =========================
# PAYMENTS
# =========================
def save_payment(telegram_id, order_id, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO payments (telegram_id, order_id, amount_usd)
        VALUES (%s, %s, %s)
    """, (telegram_id, order_id, amount))
    conn.commit()
    cur.close()
    conn.close()


def complete_payment(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE payments
        SET status='paid'
        WHERE order_id=%s
    """, (order_id,))
    conn.commit()
    cur.close()
    conn.close()
