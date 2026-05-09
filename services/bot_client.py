import httpx

BOT_API_URL = "https://cheloveckmed.ru/bot/internal/payment-success"

async def notify_payment_success(user_id: int):

    async with httpx.AsyncClient(timeout=10) as client:

        response = await client.post(
            BOT_API_URL,
            json={
                "user_id": user_id
            }
        )

        print(response.status_code)
        print(response.text)