import sqlite3
from config import DB_NAME

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    db = connect()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        language TEXT DEFAULT 'en'
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        done INTEGER DEFAULT 0
    )
    """)

    db.commit()
    db.close()

def get_language(user_id):
    db = connect()
    c = db.cursor()
    c.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        db.commit()
        lang = "en"
    else:
        lang = row[0]
    db.close()
    return lang

def set_language(user_id, lang):
    db = connect()
    c = db.cursor()
    c.execute("UPDATE users SET language=? WHERE user_id=?", (lang, user_id))
    db.commit()
    db.close()

def add_task(user_id, text):
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO tasks (user_id, text) VALUES (?,?)", (user_id, text))
    db.commit()
    db.close()
