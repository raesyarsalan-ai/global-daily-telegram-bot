import datetime
from telegram.ext import ContextTypes

from database import get_preferences


# =========================
# DAILY SMART REMINDER
# =========================
async def smart_daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id

    await context.bot.send_message(
        chat_id=chat_id,
        text="⏰ Daily Reminder\nHave a great day! 🌱"
    )


# =========================
# SETUP SCHEDULER
# =========================
def setup_scheduler(application):
    job_queue = application.job_queue

    # پیش‌فرض: ساعت ۹ صبح
    reminder_time = datetime.time(hour=9, minute=0)

    job_queue.run_daily(
        smart_daily_reminder,
        time=reminder_time,
        name="daily_smart_reminder"
    )
