import uuid
import hashlib

def create_user(telegram_id):
    username = f"user_{telegram_id}"
    password = uuid.uuid4().hex[:10]
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, username)
        VALUES (%s, %s)
        ON CONFLICT (telegram_id) DO NOTHING;
    """, (telegram_id, username))
    conn.commit()
    cur.close()
    conn.close()

    return username, password
