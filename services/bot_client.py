# import httpx
# import logging
#
# BOT_API_URL_SUCCESS = "https://cheloveckmed.ru/bot/internal/payment-success"
# BOT_API_URL_CANCELED = "https://cheloveckmed.ru/bot/internal/payment-canceled"
#
#
# async def notify_payment_success(user_id: int):
#     try:
#         async with httpx.AsyncClient(timeout=10,
#                                      verify=False
#                                      ) as client:
#
#             response = await client.post(
#                 BOT_API_URL_SUCCESS,
#                 json={"user_id": user_id}
#             )
#
#             response.raise_for_status()
#
#             logging.info(f"Bot notified: {user_id}")
#
#     except Exception as e:
#         logging.error(f"Bot notify failed: {e}")
#
#
# async def notify_payment_canceled(user_id: int):
#     try:
#         async with httpx.AsyncClient(timeout=10,
#                                      verify=False
#                                      ) as client:
#
#             response = await client.post(
#                 BOT_API_URL_CANCELED,
#                 json={"user_id": user_id}
#             )
#
#             response.raise_for_status()
#
#             logging.info(f"Bot notified: {user_id}")
#
#     except Exception as e:
#         logging.error(f"Bot notify failed: {e}")