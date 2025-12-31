from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from handlers import (
    start_handler,
    add_task_handler,
    done_task_handler,
    menu_callback_handler,
    set_language
)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("addtask", add_task_handler))
    application.add_handler(CommandHandler("donetask", done_task_handler))

    # Inline buttons
    application.add_handler(CallbackQueryHandler(menu_callback_handler, pattern="^menu_"))
    application.add_handler(CallbackQueryHandler(set_language, pattern="^setlang_"))

    application.run_polling()

if __name__ == "__main__":
    main()
