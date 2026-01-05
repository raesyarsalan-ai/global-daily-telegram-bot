# shopping.py
from database import add_shopping, get_shopping_history

def save_shopping(user_id: int, items: list[str], remind_at: str):
    if not items:
        return False
    add_shopping(user_id, "\n".join(items), remind_at)
    return True


def format_history(rows):
    if not rows:
        return None

    lines = []
    for r in rows:
        lines.append(
            f"🛒 {r[2].strftime('%Y-%m-%d')}:\n{r[1]}\n⏰ {r[3] or 'today'}"
        )
    return "\n\n".join(lines)
