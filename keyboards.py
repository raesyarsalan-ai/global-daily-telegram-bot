from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from languages import TEXTS

def t(key, lang):
    return TEXTS.get(key, {}).get(lang) or TEXTS[key]["en"]

def main_menu(lang="en"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_task", lang), callback_data="task")],
        [InlineKeyboardButton(t("btn_tasks", lang), callback_data="tasks")],
        [InlineKeyboardButton(t("btn_shop", lang), callback_data="shop")],
        [InlineKeyboardButton(t("btn_ai", lang), callback_data="ai")],
        [InlineKeyboardButton(t("btn_lang", lang), callback_data="language")],
        [InlineKeyboardButton(t("btn_help", lang), callback_data="help")],
    ])
