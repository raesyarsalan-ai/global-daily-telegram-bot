import time
from datetime import datetime, timedelta
from database import get_connection
from config import RATE_LIMIT_PER_MINUTE


def check_rate_limit(telegram_id):
    conn = get_connection()
    cur = conn.cursor()

    now = datetime.utcnow()
    reset_time = now + timedelta(minutes=1)

    cur.execute("SELECT * FROM rate_limits WHERE telegram_id=%s", (telegram_id,))
    row = cur.fetchone()

    if not row:
        cur.execute("""
            INSERT INTO rate_limits (telegram_id, count, reset_at)
            VALUES (%s, 1, %s)
        """, (telegram_id, reset_time))
        conn.commit()
        return True

    if now > row["reset_at"]:
        cur.execute("""
            UPDATE rate_limits SET count=1, reset_at=%s
            WHERE telegram_id=%s
        """, (reset_time, telegram_id))
        conn.commit()
        return True

    if row["count"] >= RATE_LIMIT_PER_MINUTE:
        return False

    cur.execute("""
        UPDATE rate_limits SET count = count + 1
        WHERE telegram_id=%s
    """, (telegram_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True


def generate_device_fingerprint(update):
    user = update.effective_user
    chat = update.effective_chat
    return f"{user.id}:{chat.type}:{user.username}"
