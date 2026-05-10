import asyncio

from fastapi import APIRouter, Request
from db.payments_repo import update_payment_status, get_payment
from datetime import datetime, timezone
from services.bot_client import notify_payment_success, notify_payment_canceled

router = APIRouter()

@router.post("/webhook/yookassa")
async def yookassa_webhook(request: Request):

    data = await request.json()
    print(data)
    event = data.get("event")
    obj = data.get("object", {})

    payment_id = obj.get("id")
    status = obj.get("status")

    # 1. ищем платеж
    payment = await get_payment(payment_id)

    if not payment:
        return {"ok": True}

    # 2. идемпотентность
    if payment[3] == status:
        return {"ok": True}

    # 3. SUCCESS
    if event == "payment.succeeded":

        await update_payment_status(
            payment_id,
            "succeeded",
            datetime.now(timezone.utc)
        )

        user_id = payment[1]
        asyncio.create_task(notify_payment_success(user_id))

    # 4. CANCEL
    elif event == "payment.canceled":

        await update_payment_status(
            payment_id,
            "canceled",
            None
        )
        user_id = payment[1]
        asyncio.create_task(notify_payment_canceled(user_id))

    return {"ok": True}