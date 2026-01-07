from handlers.subscription import buy_premium

async def callback_handler(update, context):
    data = update.callback_query.data

    if data == "buy_premium":
        await buy_premium(update, context)
