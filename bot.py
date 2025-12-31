from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from config import BOT_TOKEN
from database import init_db
import handlers

def main():
    init_db()
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(CallbackQueryHandler(handlers.callback_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handlers.text_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
