from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ask_ai")],
        [InlineKeyboardButton("📝 Add Task", callback_data="add_task")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shop")],
    ])
