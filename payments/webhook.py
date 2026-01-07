from database import activate_premium

def handle_payment_webhook(data):
    if data["status"] != "paid":
        return

    telegram_id = int(data["description"].split()[-1])
    activate_premium(telegram_id)
