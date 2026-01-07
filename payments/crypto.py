import requests
from config import CRYPTO_API_KEY

BASE_URL = "https://pay.crypt.bot/api"


def create_invoice(telegram_id, amount=10):
    res = requests.post(
        f"{BASE_URL}/createInvoice",
        headers={"Crypto-Pay-API-Token": CRYPTO_API_KEY},
        json={
            "asset": "USDT",
            "amount": amount,
            "description": f"Premium for {telegram_id}",
            "allow_comments": False
        },
        timeout=15
    )
    data = res.json()
    return data["result"] if data.get("ok") else None
