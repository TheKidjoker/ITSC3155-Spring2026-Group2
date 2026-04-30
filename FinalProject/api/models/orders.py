from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
import uuid


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    customer_name = Column(String(100))
    email = Column(String(150), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(300), nullable=True)

    order_type = Column(String(20), nullable=False)
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    description = Column(String(300))
    total_price = Column(DECIMAL(8, 2), nullable=True, server_default="0.00")

    promotion_id = Column(Integer, ForeignKey("promotions.id", ondelete="SET NULL"), nullable=True)

    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order")
    promotion = relationship("Promotion", back_populates="orders")

    tracking_id = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    order_status = Column(String(50), nullable=False, server_default="Pending")
