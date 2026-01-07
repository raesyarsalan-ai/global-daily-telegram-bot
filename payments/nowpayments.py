import requests
import uuid
from config import NOWPAYMENTS_API_KEY

BASE_URL = "https://api.nowpayments.io/v1/invoice"


def create_invoice(telegram_id, amount_usd):
    order_id = f"sub_{telegram_id}_{uuid.uuid4().hex}"

    payload = {
        "price_amount": amount_usd,
        "price_currency": "usd",
        "pay_currency": "usdt",
        "order_id": order_id
    }

    headers = {
        "x-api-key": NOWPAYMENTS_API_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(BASE_URL, json=payload, headers=headers, timeout=15)
    res.raise_for_status()
    return res.json(), order_id
