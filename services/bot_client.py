import httpx
import logging

BOT_API_URL = "https://cheloveckmed.ru/bot/internal/payment-success"


async def notify_payment_success(user_id: int):

    try:
        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.post(
                BOT_API_URL,
                json={"user_id": user_id}
            )

            response.raise_for_status()

            logging.info(f"Bot notified: {user_id}")

    except Exception as e:
        logging.error(f"Bot notify failed: {e}")