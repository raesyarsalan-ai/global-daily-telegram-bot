from telegram import Update
from telegram.ext import ContextTypes
from database import get_language, set_language, add_task, add_shopping_item
from languages import TEXTS
from keyboards import main_menu, language_menu
from ai import ask_ai, parse_shopping_text


def t(key, lang):
    return TEXTS.get(key, {}).get(lang) or TEXTS[key]["en"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_language(user_id)
    await update.message.reply_text(
        t("start", lang),
        reply_markup=main_menu(lang)
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang = get_language(user_id)
    data = query.data

    if data == "language":
        await query.edit_message_text(
            "🌐 Choose language:",
            reply_markup=language_menu()
        )

    elif data.startswith("lang_"):
        code = data.split("_")[1]
        set_language(user_id, code)
        await query.edit_message_text(
            "✅ Language updated",
            reply_markup=main_menu(code)
        )

    elif data == "task":
        context.user_data["mode"] = "task"
        await query.edit_message_text(t("ask_task", lang))

    elif data == "shopping":
        context.user_data["mode"] = "shopping"
        await query.edit_message_text(t("ask_shop", lang))

    elif data == "ai":
        context.user_data["mode"] = "ai"
        await query.edit_message_text("🤖 Ask me anything:")


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_language(user_id)
    text = update.message.text
    mode = context.user_data.get("mode")

    if mode == "task":
        add_task(user_id, text)
        await update.message.reply_text(
            t("task_added", lang),
            reply_markup=main_menu(lang)
        )
        context.user_data["mode"] = None

    elif mode == "shopping":
        result = await parse_shopping_text(text)
        for item in result.get("items", []):
            add_shopping_item(user_id, item, result.get("remind_at"))

        await update.message.reply_text(
            t("shop_saved", lang),
            reply_markup=main_menu(lang)
        )
        context.user_data["mode"] = None

    elif mode == "ai":
        await update.message.reply_text(t("ai_thinking", lang))
        reply = await ask_ai(text)
        await update.message.reply_text(
            reply,
            reply_markup=main_menu(lang)
        )
