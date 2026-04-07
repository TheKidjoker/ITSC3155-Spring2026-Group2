from typing import Optional

from pydantic import BaseModel


class PromotionBase(BaseModel):
    code: str
    discount_percent: int
    description: Optional[str] = None
    active: bool = True


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    discount_percent: Optional[int] = None
    description: Optional[str] = None
    active: Optional[bool] = None


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True
