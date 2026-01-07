from datetime import datetime, timedelta
from database import get_connection


def add_task(telegram_id: int, title: str, schedule: str):
    """
    schedule: daily | weekly | monthly
    """
    now = datetime.utcnow()

    if schedule == "daily":
        due = now + timedelta(days=1)
    elif schedule == "weekly":
        due = now + timedelta(days=7)
    elif schedule == "monthly":
        due = now + timedelta(days=30)
    else:
        due = None

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tasks (telegram_id, title, schedule, due_at)
        VALUES (%s, %s, %s, %s)
    """, (telegram_id, title, schedule, due))
    conn.commit()
    cur.close()
    conn.close()
