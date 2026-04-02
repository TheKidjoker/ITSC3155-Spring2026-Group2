from sqlalchemy import Column, Integer, String, Float
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)   
    price = Column(Float, nullable=False)
    calories = Column(Integer)
    category = Column(String(100))               