import os
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from handlers import start, handle_message
# از الان آماده DB و scheduler هستیم
# from database import init_db
# from scheduler import start_scheduler


BOT_TOKEN = os.getenv("BOT_TOKEN")


async def on_startup(app: Application):
    """
    Runs once when bot starts
    """
    print("🚀 Bot starting...")

    # اگر DB فعال شد، فقط این خط را uncomment کن
    # await init_db()

    # اگر scheduler اضافه شد
    # start_scheduler(app)

    print("✅ Startup completed")


async def on_shutdown(app: Application):
    """
    Runs once when bot stops
    """
    print("🛑 Bot shutting down...")


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(on_startup)
        .post_shutdown(on_shutdown)
        .build()
    )

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Text messages (buttons & free text)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
