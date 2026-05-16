from fastapi import APIRouter

from schemas import (
    CreatePaymentRequest,
    CreatePaymentResponse, RemovePaymentRequest, RemovePaymentResponse
)

from yookassa_service import create_payment, send_notify_complete

router = APIRouter()


@router.post(
    "/create-payment",
    response_model=CreatePaymentResponse
)
async def create_payment_route(
    data: CreatePaymentRequest
):

    payment = await create_payment(
        amount=data.amount,
        user_id=data.user_id,
        user_email= data.user_email,
        description=data.description
    )

    return payment

@router.post(
    "/remove-payment",
    response_model=RemovePaymentResponse
)
async def create_payment_route(
    data: RemovePaymentRequest
):
    payment_id = data.payment_id
    return await send_notify_complete(payment_id)


