import asyncio
from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from database import init_db
from handlers import (
    start_handler,
    add_task_handler,
    list_tasks_handler,
    done_task_handler
)


async def main():
    # init database (SYNC function → no await)
    init_db()

    application = Application.builder().token(BOT_TOKEN).build()

    # basic
    application.add_handler(CommandHandler("start", start_handler))

    # tasks
    application.add_handler(CommandHandler("addtask", add_task_handler))
    application.add_handler(CommandHandler("tasks", list_tasks_handler))
    application.add_handler(CommandHandler("donetask", done_task_handler))

    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
