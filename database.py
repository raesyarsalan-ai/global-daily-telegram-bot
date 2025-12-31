import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                done INTEGER DEFAULT 0
            )""")
conn.commit()

def add_task(user_id, text):
    c.execute("INSERT INTO tasks (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()

def get_tasks(user_id):
    c.execute("SELECT id, text, done FROM tasks WHERE user_id=?", (user_id,))
    return c.fetchall()

def mark_task_done(task_id, user_id):
    c.execute("UPDATE tasks SET done=1 WHERE id=? AND user_id=?", (task_id, user_id))
    conn.commit()
