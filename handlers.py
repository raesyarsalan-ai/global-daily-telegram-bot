from telegram import Update
from telegram.ext import ContextTypes
from database import add_task, get_tasks, mark_task_done


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Commands:\n"
        "/addtask Buy milk\n"
        "/tasks\n"
        "/donetask 1"
    )


async def add_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /addtask Buy milk")
        return

    user_id = update.effective_user.id
    text = " ".join(context.args)

    add_task(user_id, text)
    await update.message.reply_text("✅ Task added")


async def list_tasks_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = get_tasks(user_id)

    if not tasks:
        await update.message.reply_text("📝 You have no tasks.")
        return

    message = "📝 Your tasks:\n\n"
    for task_id, text, is_done in tasks:
        status = "✅" if is_done else "⏳"
        message += f"{task_id}. {status} {text}\n"

    await update.message.reply_text(message)


async def done_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /donetask 1")
        return

    user_id = update.effective_user.id

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Task id must be a number.")
        return

    mark_task_done(task_id, user_id)
    await update.message.reply_text("✅ Task marked as done")
