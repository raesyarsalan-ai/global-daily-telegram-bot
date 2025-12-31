import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from config import BOT_TOKEN
from database import init_db
import handlers


async def main():
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CallbackQueryHandler(handlers.callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.text_handler))

    print("🤖 Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
