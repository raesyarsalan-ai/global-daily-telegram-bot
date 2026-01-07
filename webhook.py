import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException
from database import complete_payment, activate_premium
from config import NOWPAYMENTS_IPN_SECRET

app = FastAPI()


@app.post("/nowpayments-ipn")
async def nowpayments_ipn(request: Request):
    body = await request.body()
    sig = request.headers.get("x-nowpayments-sig")

    check = hmac.new(
        NOWPAYMENTS_IPN_SECRET.encode(),
        body,
        hashlib.sha512
    ).hexdigest()

    if sig != check:
        raise HTTPException(status_code=403)

    data = await request.json()

    if data.get("payment_status") == "finished":
        order_id = data["order_id"]
        telegram_id = int(order_id.split("_")[1])

        complete_payment(order_id)
        activate_premium(telegram_id, 30)

    return {"ok": True}
