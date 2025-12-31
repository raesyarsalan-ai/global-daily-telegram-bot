import sqlite3
from datetime import datetime

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

# users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    language TEXT DEFAULT 'en',
    subscription INTEGER DEFAULT 0,
    sub_expire TEXT
)
""")

# tasks
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    is_done INTEGER DEFAULT 0
)
""")

# shopping
cursor.execute("""
CREATE TABLE IF NOT EXISTS shopping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    is_done INTEGER DEFAULT 0
)
""")

conn.commit()

def set_user_language(user_id, lang):
    cursor.execute("INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", (user_id, lang))
    conn.commit()

def get_user_language(user_id):
    cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else "en"

# task
def add_task(user_id, text):
    cursor.execute("INSERT INTO tasks (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()

def get_tasks(user_id):
    cursor.execute("SELECT id, text, is_done FROM tasks WHERE user_id=?", (user_id,))
    return cursor.fetchall()

def mark_task_done(task_id, user_id):
    cursor.execute("UPDATE tasks SET is_done=1 WHERE id=? AND user_id=?", (task_id, user_id))
    conn.commit()

# shopping
def add_shopping(user_id, text):
    cursor.execute("INSERT INTO shopping (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()

def get_shopping(user_id):
    cursor.execute("SELECT id, text, is_done FROM shopping WHERE user_id=?", (user_id,))
    return cursor.fetchall()

def mark_shopping_done(item_id, user_id):
    cursor.execute("UPDATE shopping SET is_done=1 WHERE id=? AND user_id=?", (item_id, user_id))
    conn.commit()
