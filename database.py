import psycopg2
import uuid
import datetime
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# =========================
# Connection
# =========================
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


# =========================
# Init DB (tables)
# =========================
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE NOT NULL,
        username TEXT,
        password_hash TEXT,
        is_premium BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # sessions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        telegram_id BIGINT PRIMARY KEY,
        token TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------- Phase 1 ----------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_checkins (
        telegram_id BIGINT,
        checkin_date DATE,
        PRIMARY KEY (telegram_id, checkin_date)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_activity (
        telegram_id BIGINT PRIMARY KEY,
        activity_count INTEGER DEFAULT 0,
        last_activity TIMESTAMP
    )
    """)

    # ---------- Phase 2 ----------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_mood (
        telegram_id BIGINT PRIMARY KEY,
        mood TEXT,
        updated_at TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_preferences (
        telegram_id BIGINT PRIMARY KEY,
        preferred_tone TEXT DEFAULT 'friendly',
        reminder_hour INTEGER DEFAULT 9
    )
    """)

    # ---------- Phase 3 ----------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS referrals (
        telegram_id BIGINT PRIMARY KEY,
        referral_code TEXT UNIQUE,
        invited_by BIGINT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        telegram_id BIGINT,
        badge TEXT,
        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (telegram_id, badge)
    )
    """)

    conn.commit()
