from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items" #table name

    #primary key
    id = Column(Integer, primary_key=True, index=True, autoIncrement=True)

    #item name
    item_name = Column(String(100), nullable=False, unique=True)
    #price
    price = Column(DECIMAL(6,2), nullable=False, server_default='0.0')
    #calories
    calories = Column(Integer, nullable=True)
    #category
    food_category= Column(String(50), nullable=True)
    #description
    description=Column(String(300), nullable=True)

    #relationship to order_details
    order_details = relationship("OrderDetail", back_populates="menu_item")
