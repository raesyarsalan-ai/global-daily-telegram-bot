import psycopg2
from datetime import datetime
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS shopping (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        items TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        remind_at TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        text TEXT NOT NULL,
        done BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


def add_shopping(user_id, items, remind):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO shopping (user_id, items, remind_at)
        VALUES (%s, %s, %s);
    """, (user_id, items, remind))
    conn.commit()
    cur.close()
    conn.close()


def get_shopping_history(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, items, created_at, remind_at
        FROM shopping
        WHERE user_id = %s
        ORDER BY created_at DESC;
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def add_task(user_id, text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tasks (user_id, text)
        VALUES (%s, %s);
    """, (user_id, text))
    conn.commit()
    cur.close()
    conn.close()


def get_tasks(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, text, done, created_at
        FROM tasks
        WHERE user_id = %s
        ORDER BY created_at DESC;
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def set_task_done(user_id, task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE tasks
        SET done = TRUE
        WHERE id = %s AND user_id = %s;
    """, (task_id, user_id))
    conn.commit()
    cur.close()
    conn.close()
