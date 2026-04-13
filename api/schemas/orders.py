from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_name: str
    email: Optional[str] = None
    description: Optional[str] = None
    order_type: str
    address: Optional[str] = None
    promotion_id: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    order_type: Optional[str] = None
    address: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    promotion_id: Optional[int] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_id: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True

class GuestOrder(BaseModel):
    customer_name: str
    email: Optional[str] = None
    phone: str
    address: str
    sandwich_id: int
    quantity: int = 1