from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu
from database import save_shopping_list, set_shopping_reminder
from ai import clean_shopping_list
from datetime import datetime


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to DailyHelperBot",
        reply_markup=main_menu()
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "shop":
        context.user_data["mode"] = "shop_input"
        await query.edit_message_text(
            "🛒 Please send your shopping list (you can send a long list):"
        )

    elif query.data == "ai":
        context.user_data["mode"] = "ai"
        await query.edit_message_text("🤖 Ask me anything:")


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    mode = context.user_data.get("mode")

    # 🛒 مرحله 1 و 2 و 3
    if mode == "shop_input":
        cleaned = await clean_shopping_list(text, "en")

        entry = save_shopping_list(
            user_id=user_id,
            raw_text=text,
            ai_list=cleaned
        )

        context.user_data["mode"] = "shop_reminder"

        await update.message.reply_text(
            f"✅ Shopping list saved!\n\n{cleaned}\n\n"
            "🕒 Do you want to buy this **today** or **another date**?\n"
            "✍️ If another date, please write the exact date.",
            reply_markup=main_menu()
        )
        return

    # ⏰ مرحله 4 – یادآوری
    if mode == "shop_reminder":
        if "today" in text.lower():
            set_shopping_reminder(user_id, "today")

            context.user_data["mode"] = None
            await update.message.reply_text(
                "🛒 Got it! Today shopping noted.\n"
                f"📅 Created at: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                reply_markup=main_menu()
            )
            return

        else:
            set_shopping_reminder(user_id, text)

            context.user_data["mode"] = None
            await update.message.reply_text(
                f"⏰ Reminder set for:\n{text}\n"
                f"📅 Created at: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                reply_markup=main_menu()
            )
            return

    # 🤖 AI chat
    if mode == "ai":
        await update.message.reply_text("🤖 (AI logic here)")
        return

    await update.message.reply_text("Use the menu 👇", reply_markup=main_menu())
