import sqlite3

DB_NAME = "daily_helper.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'en'
        )
    """)

    # tasks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            done INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# ---------- Language ----------
def get_language(user_id: int) -> str:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    if row:
        lang = row[0]
    else:
        lang = "en"
        cur.execute(
            "INSERT INTO users (user_id, language) VALUES (?, ?)",
            (user_id, lang)
        )
        conn.commit()

    conn.close()
    return lang


def set_language(user_id: int, language: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (user_id, language)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET language=excluded.language
    """, (user_id, language))

    conn.commit()
    conn.close()


# ---------- Tasks ----------
def add_task(user_id: int, title: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (user_id, title) VALUES (?, ?)",
        (user_id, title)
    )

    conn.commit()
    conn.close()


def get_tasks(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title, done FROM tasks WHERE user_id=?",
        (user_id,)
    )
    tasks = cur.fetchall()

    conn.close()
    return tasks


def mark_task_done(task_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET done=1 WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()
