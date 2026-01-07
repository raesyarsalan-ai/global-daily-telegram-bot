from datetime import datetime
from database import get_connection


def add_reminder(telegram_id: int, text: str, remind_at: datetime):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reminders (telegram_id, text, remind_at)
        VALUES (%s, %s, %s)
    """, (telegram_id, text, remind_at))
    conn.commit()
    cur.close()
    conn.close()
