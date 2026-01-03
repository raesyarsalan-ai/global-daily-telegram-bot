import sqlite3
from datetime import datetime

DB_NAME = "bot.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    db = connect()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS shopping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        items TEXT,
        created_at TEXT,
        reminder TEXT
    )
    """)

    db.commit()
    db.close()

def save_shopping(user_id, items):
    db = connect()
    c = db.cursor()
    c.execute(
        "INSERT INTO shopping (user_id, items, created_at) VALUES (?,?,?)",
        (user_id, items, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    db.commit()
    db.close()

def set_reminder(user_id, reminder):
    db = connect()
    c = db.cursor()
    c.execute(
        "UPDATE shopping SET reminder=? WHERE user_id=? ORDER BY id DESC LIMIT 1",
        (reminder, user_id)
    )
    db.commit()
    db.close()
