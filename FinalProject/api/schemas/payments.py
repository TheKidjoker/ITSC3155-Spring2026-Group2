from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    method: str = "card"
    status: str = "pending"


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    method: Optional[str] = None
    status: Optional[str] = None


class Payment(PaymentBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
