from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers import start, callback_handler, text_handler
from database import init_db
from scheduler import setup_scheduler


def main():
    # =========================
    # Init Database
    # =========================
    init_db()

    # =========================
    # Build Application
    # =========================
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # =========================
    # Setup Scheduler (Smart Reminder)
    # =========================
    setup_scheduler(app)

    # =========================
    # Handlers
    # =========================
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    # =========================
    # Run Bot
    # =========================
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
