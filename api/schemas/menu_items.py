#response and request format

from typing import Optional
from pydantic import BaseModel


class MenuItemBase(BaseModel):
    item_name: str
    price: float
    calories: Optional[int] = None
    food_category: Optional[str] = None
    description: Optional[str] = None

class MenuItemCreate(MenuItemBase):
    #pass
    pass

class MenuItemUpdate(BaseModel):
    #used for updating menu items
    item_name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    food_category: Optional[str] = None
    description: Optional[str] = None

class MenuItem(MenuItemBase):
    id: int

    class Config:
        from_attributes = True