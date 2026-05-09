from fastapi import APIRouter

from schemas import (
    CreatePaymentRequest,
    CreatePaymentResponse
)

from yookassa_service import create_payment

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

