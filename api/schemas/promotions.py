from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PromotionBase(BaseModel):
    code: str
    discount_percentage: Optional[float] = None
    discount_amount: Optional[float] = None
    expiration_date: Optional[datetime] = None
    is_active: Optional[bool] = True


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    discount_percentage: Optional[float] = None
    discount_amount: Optional[float] = None
    expiration_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True


class ApplyPromoCode(BaseModel):
    code: str
    order_total: float


class ApplyPromoCodeResponse(BaseModel):
    code: str
    discount_percentage: Optional[float] = None
    discount_amount: Optional[float] = None
    new_total: float
