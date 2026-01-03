import sqlite3
from datetime import datetime
from config import DB_PATH

def connect_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    db = connect_db()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS shopping (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        items TEXT,
        created_at TEXT,
        remind_at TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        text TEXT,
        done INTEGER DEFAULT 0,
        created_at TEXT
    )
    """)

    db.commit()
    db.close()

def add_shopping(user_id, items, remind):
    db = connect_db()
    db.cursor().execute("INSERT INTO shopping (user_id, items, created_at, remind_at) VALUES(?,?,?,?)",
                         (user_id, items, datetime.now().strftime("%Y-%m-%d %H:%M"), remind))
    db.commit()
    db.close()

def get_shopping_history(user_id):
    db = connect_db()
    c = db.cursor()
    c.execute("SELECT id, items, created_at, remind_at FROM shopping WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    db.close()
    return rows

def add_task(user_id, text):
    db = connect_db()
    db.cursor().execute("INSERT INTO tasks (user_id, text, created_at) VALUES(?,?,?)",
                         (user_id, text, datetime.now().strftime("%Y-%m-%d %H:%M")))
    db.commit()
    db.close()

def get_tasks(user_id):
    db = connect_db()
    c = db.cursor()
    c.execute("SELECT id,text,done,created_at FROM tasks WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    db.close()
    return rows

def set_task_done(user_id, task_id):
    db = connect_db()
    db.cursor().execute("UPDATE tasks SET done=1 WHERE id=? AND user_id=?", (task_id,user_id))
    db.commit()
    db.close()
