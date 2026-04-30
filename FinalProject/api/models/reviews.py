from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, func
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=True)
    customer_name = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String(500), nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())

    order = relationship("Order")
    menu_item = relationship("MenuItem")
