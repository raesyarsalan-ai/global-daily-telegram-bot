import requests
from config import CRYPTO_API_KEY

NOW_URL = "https://api.nowpayments.io/v1/invoice"

def create_crypto_invoice(amount_usd, order_id):
    headers = {"x-api-key": CRYPTO_API_KEY}
    data = {
        "price_amount": amount_usd,
        "price_currency": "usd",
        "pay_currency": "usdt",
        "order_id": order_id,
        "ipn_callback_url": "",
    }
    res = requests.post(NOW_URL, json=data, headers=headers)
    return res.json()
