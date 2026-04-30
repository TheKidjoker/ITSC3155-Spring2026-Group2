from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    order_id: int
    payment_type: str
    transaction_status: str
    card_number: Optional[str] = None
    payment_amount: float


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    payment_type: Optional[str] = None
    transaction_status: Optional[str] = None
    card_number: Optional[str] = None
    payment_amount: Optional[float] = None


class Payment(PaymentBase):
    id: int
    payment_date: Optional[datetime] = None

    class Config:
        from_attributes = True
