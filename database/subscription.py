from datetime import datetime
from database import get_connection


def set_subscription(telegram_id: int, expires_at: datetime):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO subscriptions (telegram_id, expires_at)
        VALUES (%s, %s)
        ON CONFLICT (telegram_id)
        DO UPDATE SET expires_at = EXCLUDED.expires_at
    """, (telegram_id, expires_at))
    conn.commit()
    cur.close()
    conn.close()


def is_premium(telegram_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT expires_at FROM subscriptions WHERE telegram_id=%s",
        (telegram_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return False
    return row[0] > datetime.utcnow()
