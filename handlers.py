from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu
from languages import LANGUAGES
from ai import ask_ai
from database import save_shopping, set_reminder

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = "en"
    context.user_data["lang"] = lang
    await update.message.reply_text(
        LANGUAGES[lang]["welcome"],
        reply_markup=main_menu()
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "ask_ai":
        context.user_data["mode"] = "ai_chat"
        await query.message.reply_text("🤖 Ask your question:")

    elif data == "add_task":
        context.user_data["mode"] = "add_task"
        await query.message.reply_text("📝 Send your task:")

    elif data == "shop":
        context.user_data["mode"] = "shop_items"
        await query.message.reply_text(
            "🛒 Please send your shopping list (you can send a long list):"
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")
    user_id = update.effective_user.id

    if mode == "ai_chat":
        answer = await ask_ai(text)
        await update.message.reply_text(answer)
        return

    if mode == "add_task":
        await update.message.reply_text(f"✅ Task saved:\n{text}")
        return

    # 🛒 مرحله 1: ذخیره لیست خرید
    if mode == "shop_items":
        save_shopping(user_id, text)
        context.user_data["mode"] = "shop_time"
        await update.message.reply_text(
            "✅ Shopping list saved.\n"
            "🕒 Will you buy it **today** or **another date**?\n"
            "If another date, please write the exact date."
        )
        return

    # 🛒 مرحله 2: زمان خرید
    if mode == "shop_time":
        if "today" in text.lower():
            set_reminder(user_id, "today")
            await update.message.reply_text(
                "🛒 Noted! Today shopping saved.",
                reply_markup=main_menu()
            )
        else:
            set_reminder(user_id, text)
            await update.message.reply_text(
                f"⏰ Reminder set for: {text}",
                reply_markup=main_menu()
            )
        context.user_data["mode"] = None
        return

    await update.message.reply_text("Use the menu 👇", reply_markup=main_menu())
