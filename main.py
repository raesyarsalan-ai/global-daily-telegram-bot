from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from config import BOT_TOKEN
from database import init_db
from handlers.start import start
from handlers.admin import admin_panel


def main():
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))

    print("🤖 Bot is running securely...")
    app.run_polling()


if __name__ == "__main__":
    main()
