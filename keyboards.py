from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ai")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shop")],
        [InlineKeyboardButton("📝 Tasks", callback_data="tasks")],
        [InlineKeyboardButton("🌐 Language", callback_data="language")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
    ])


def shopping_time_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🕒 Today", callback_data="shop_today")],
        [InlineKeyboardButton("📅 Choose date", callback_data="shop_date")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_menu")],
    ])


def tasks_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Task", callback_data="task_add")],
        [InlineKeyboardButton("📋 View Tasks", callback_data="task_list")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_menu")],
    ])


def language_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("English 🇺🇸", callback_data="lang_en")],
        [InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang_fa")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_menu")],
    ])
