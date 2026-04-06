from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    customer_name: str
    rating: int = Field(ge=1, le=5)
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    customer_name: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
