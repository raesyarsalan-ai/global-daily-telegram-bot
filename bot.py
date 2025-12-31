from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
from config import BOT_TOKEN, ADMIN_IDS
import scheduler

from handlers import (
    start_handler, language_handler, menu_handler,
    add_task_handler, list_tasks_handler, done_task_handler,
    add_shopping_handler, list_shopping_handler, done_shopping_handler
)
from ai import chat_ai
from payments import create_crypto_invoice
from admin import view_users

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # پایه
    app.add_handler(CommandHandler("start", start_handler))

    # TASK
    app.add_handler(CommandHandler("addtask", add_task_handler))
    app.add_handler(CommandHandler("tasks", list_tasks_handler))
    app.add_handler(CommandHandler("donetask", done_task_handler))

    # SHOPPING
    app.add_handler(CommandHandler("addshopping", add_shopping_handler))
    app.add_handler(CommandHandler("shopping", list_shopping_handler))
    app.add_handler(CommandHandler("doneshopping", done_shopping_handler))

    # AI
    async def ai_handler(update, context):
        prompt = " ".join(context.args)
        response = await chat_ai(prompt)
        await update.message.reply_text(response)

    app.add_handler(CommandHandler("ai", ai_handler))

    # Subscription
    async def subscribe_handler(update, context):
        invoice = create_crypto_invoice(10, str(update.effective_user.id))
        await update.message.reply_text(f"Pay:\n{invoice['invoice_url']}")

    app.add_handler(CommandHandler("subscribe", subscribe_handler))

    # Admin
    app.add_handler(CommandHandler("users", view_users))

    # Callbacks
    app.add_handler(CallbackQueryHandler(language_handler, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^menu_"))

    # Scheduler
    scheduler.setup_scheduler(app)

    app.run_polling()

if __name__ == "__main__":
    main()
