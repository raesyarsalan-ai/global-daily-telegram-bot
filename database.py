# ⬅️ کل محتوای قبلی حفظ شده + این بخش اضافه شده (کامل فایل)

def get_all_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT telegram_id, is_premium FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def set_premium_status(telegram_id: int, status: bool):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET is_premium=%s WHERE telegram_id=%s",
        (status, telegram_id),
    )
    conn.commit()
    cur.close()
    conn.close()
