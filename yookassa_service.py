import uuid
import asyncio
from db.payments_repo import create_payment_record
from yookassa import Configuration, Payment
from config import (
    YOOKASSA_SHOP_ID,
    YOOKASSA_SECRET_KEY
)


Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


async def create_payment(
    amount: int,
    user_id: int,
    user_email: str,
    description: str

):
    payload = {
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": "https://max.ru/id6166083531_bot"
        },
        "description": description,

        "metadata": {
            "user_id": user_id
        },

        "receipt": {
            "customer": {
                "email": user_email
            },
            "items": [
                {
                    "description": description,
                    "quantity": "1.00",
                    "amount": {
                        "value": f"{amount:.2f}",
                        "currency": "RUB"
                    },
                    "vat_code": 6,
                    "payment_mode": "full_payment",
                    "payment_subject": "service"
                }
            ]
        }
    }

    idempotence_key = str(uuid.uuid4())

    payment = await asyncio.to_thread(
        Payment.create,
        payload,
        idempotence_key
    )

    await create_payment_record(
        payment_id=payment.id,
        user_id=user_id,
        amount=amount,
        status=payment.status
    )
    print(payment)

    return {
        "payment_id": payment.id,
        "confirmation_url": payment.confirmation.confirmation_url,
        "status": payment.status
    }