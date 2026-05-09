from fastapi import APIRouter, Request
from db.payments_repo import update_payment_status, get_payment
from datetime import datetime, timezone
from services.bot_client import notify_payment_success

router = APIRouter()


@router.post("/webhook/yookassa")
async def yookassa_webhook(request: Request):

    data = await request.json()

    event = data.get("event")
    obj = data.get("object", {})

    payment_id = obj.get("id")
    status = obj.get("status")

    # защита от мусора
    payment = await get_payment(payment_id)
    if not payment:
        return {"ok": True}

    # идемпотентность
    if payment[3] == status:  # status уже такой же
        return {"ok": True}

    if event == "payment.succeeded":
        await update_payment_status(payment_id, "succeeded", datetime.now(timezone.utc))
        user_id = payment[1]

        await notify_payment_success(user_id)


        # тут дальше будет:
        # 👉 выдача доступа в боте

    elif event == "payment.canceled":
        await update_payment_status(payment_id, "canceled", None)

    return {"ok": True}