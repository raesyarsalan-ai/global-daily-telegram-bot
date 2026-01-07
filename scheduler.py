import datetime
from telegram.ext import ContextTypes
from database import get_connection


async def reminder_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    data = job.data

    await context.bot.send_message(
        chat_id=data["telegram_id"],
        text=f"⏰ Reminder:\n{data['text']}"
    )


def setup_scheduler(application):
    job_queue = application.job_queue

    # Load future reminders from DB on startup
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT telegram_id, text, remind_at
        FROM reminders
        WHERE remind_at > NOW()
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for r in rows:
        job_queue.run_once(
            reminder_job,
            when=r["remind_at"],
            data={
                "telegram_id": r["telegram_id"],
                "text": r["text"]
            }
        )
