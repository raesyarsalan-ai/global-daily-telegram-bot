from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers import start, callback_handler, text_handler
from database import init_db   # ✅ اضافه شده (مرحله 1)

def main():
    # ✅ مقداردهی اولیه دیتابیس (ایجاد جدول‌ها اگر وجود ندارند)
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
