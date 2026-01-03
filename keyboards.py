from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 AI Chat", callback_data="ai")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shop")],
        [InlineKeyboardButton("📋 Shopping History", callback_data="shop_history")],
        [InlineKeyboardButton("📝 Tasks", callback_data="tasks")],
    ])

def tasks_menu(tasks):
    buttons = []
    for t in tasks:
        buttons.append([InlineKeyboardButton(f"{t[1]} ({'Done' if t[2] else 'Pending'})", callback_data=f"task_{t[0]}")])
    return InlineKeyboardMarkup(buttons)
