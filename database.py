from datetime import datetime

# ذخیره در حافظه (بعداً قابل تبدیل به DB واقعی)
SHOPPING_LISTS = {}     # user_id -> list
SHOPPING_HISTORY = {}  # user_id -> list


def save_shopping_list(user_id: int, raw_text: str, ai_list: str):
    entry = {
        "raw": raw_text,
        "clean": ai_list,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "reminder": None,
    }

    SHOPPING_LISTS.setdefault(user_id, []).append(entry)
    SHOPPING_HISTORY.setdefault(user_id, []).append(entry)

    return entry


def set_shopping_reminder(user_id: int, reminder_text: str):
    if user_id in SHOPPING_LISTS and SHOPPING_LISTS[user_id]:
        SHOPPING_LISTS[user_id][-1]["reminder"] = reminder_text


def get_shopping_history(user_id: int):
    return SHOPPING_HISTORY.get(user_id, [])
