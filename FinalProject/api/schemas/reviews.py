from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    customer_name: str
    rating: int
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    customer_name: Optional[str] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
