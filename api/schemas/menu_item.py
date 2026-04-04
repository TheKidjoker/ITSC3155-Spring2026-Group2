from pydantic import BaseModel

class MenuItemResponse(BaseModel):
    id: int
    name: str
    price: float
    calories: int
    category: str

    class Config:
        from_attributes = True   # for Pydantic v2