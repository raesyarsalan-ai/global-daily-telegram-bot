from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers import (
    start_handler,
    add_task_handler,
    list_tasks_handler,
    done_task_handler,
)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("addtask", add_task_handler))
    application.add_handler(CommandHandler("tasks", list_tasks_handler))
    application.add_handler(CommandHandler("donetask", done_task_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
