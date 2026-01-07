from handlers.ai_handler import ai_handler
from handlers.subscription import buy_premium


async def callback_handler(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "ai":
        await query.message.reply_text("🤖 Ask me anything:")
        context.user_data["mode"] = "ai"

    elif query.data == "buy_premium":
        await buy_premium(update, context)
