from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu, shopping_time_menu
from languages import LANGUAGES
from ai import ask_ai
from storage import save_shopping

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lang"] = "en"
    await update.message.reply_text(
        LANGUAGES["en"]["welcome"],
        reply_markup=main_menu()
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "ask_ai":
        context.user_data["mode"] = "ai"
        await q.message.reply_text("🤖 Ask anything:")

    elif q.data == "shopping":
        context.user_data["mode"] = "shopping"
        await q.message.reply_text("🛒 Send your shopping list:")

    elif q.data == "shop_today":
        items = context.user_data.pop("shopping_items", [])
        save_shopping(q.from_user.id, items)
        await q.message.reply_text("✅ Shopping list saved. I will remind you today.")

    elif q.data == "shop_later":
        context.user_data["mode"] = "shopping_time"
        await q.message.reply_text("📅 Please send reminder date & time:")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")

    if mode == "ai":
        reply = await ask_ai(text)
        await update.message.reply_text(reply)

    elif mode == "shopping":
        items = [x.strip() for x in text.split("\n")]
        context.user_data["shopping_items"] = items
        await update.message.reply_text(
            "🛒 List saved. When should I remind you?",
            reply_markup=shopping_time_menu()
        )

    elif mode == "shopping_time":
        save_shopping(update.effective_user.id,
                      context.user_data.get("shopping_items", []),
                      remind_at=text)
        await update.message.reply_text("✅ List saved. I will remind you at the selected time.")
