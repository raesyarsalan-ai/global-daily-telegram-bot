from telegram.ext import JobQueue
from database import get_tasks

async def daily_reminder(context):
    job = context.job
    tasks = get_tasks(job.chat_id)
    if tasks:
        text = "Daily Reminder:\n"
        for i, t, d in tasks:
            if d == 0: text += f"{i}. {t}\n"
        await context.bot.send_message(chat_id=job.chat_id, text=text)

def setup_scheduler(application):
    jq = application.job_queue
    jq.run_daily(daily_reminder, time=datetime.time(hour=9, minute=0))
