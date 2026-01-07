from database.subscription import is_premium

# داخل بخش AI:
if mode == "ai":
    if not is_premium(user_id):
        await update.message.reply_text(
            "⭐ Free users have limited AI.\nUpgrade to Premium."
        )
        return

    reply = await ask_ai(text)
    await update.message.reply_text(reply)
