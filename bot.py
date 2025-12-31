import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from handlers import start, handle_message

BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
