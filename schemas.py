from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    amount: int
    user_id: int
    user_email:str
    description: str


class CreatePaymentResponse(BaseModel):
    payment_id: str
    confirmation_url: str
    status: str