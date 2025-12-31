from telegram import Update
from telegram.ext import ContextTypes

async def view_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database import cursor
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    await update.message.reply_text(f"Users:\n" + "\n".join(str(u[0]) for u in users))
