from datetime import datetime

SHOPPING_DB = {}

def save_shopping(user_id, items, remind_at=None):
    SHOPPING_DB.setdefault(user_id, [])
    SHOPPING_DB[user_id].append({
        "items": items[:1000],
        "created_at": datetime.now(),
        "remind_at": remind_at
    })
