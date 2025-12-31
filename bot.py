from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from config import BOT_TOKEN
from handlers import (
    start_handler,
    add_task_handler,
    list_tasks_handler,
    done_task_handler,
    language_callback,
)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("addtask", add_task_handler))
    application.add_handler(CommandHandler("tasks", list_tasks_handler))
    application.add_handler(CommandHandler("donetask", done_task_handler))

    # Callback handler برای دکمه‌ها
    application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))

    application.run_polling()

if __name__ == "__main__":
    main()
