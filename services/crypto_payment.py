import requests
from config import CRYPTO_API_KEY


class CryptoPaymentService:
    BASE_URL = "https://pay.crypt.bot/api"

    def __init__(self):
        self.headers = {
            "Crypto-Pay-API-Token": CRYPTO_API_KEY,
            "Content-Type": "application/json",
        }

    def create_invoice(
        self,
        amount: float,
        asset: str = "USDT",
        description: str = "Premium Subscription",
    ):
        url = f"{self.BASE_URL}/createInvoice"
        payload = {
            "asset": asset,
            "amount": amount,
            "description": description,
            "allow_comments": False,
            "allow_anonymous": False,
        }

        response = requests.post(url, json=payload, headers=self.headers, timeout=15)
        data = response.json()

        if not data.get("ok"):
            return None

        return data["result"]

    def get_invoice_status(self, invoice_id: int):
        url = f"{self.BASE_URL}/getInvoices"
        payload = {"invoice_ids": [invoice_id]}

        response = requests.post(url, json=payload, headers=self.headers, timeout=15)
        data = response.json()

        if not data.get("ok") or not data["result"]["items"]:
            return None

        return data["result"]["items"][0]
