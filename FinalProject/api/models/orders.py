from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
import uuid

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)

    #Guest detailds
    customer_name = Column(String(100))
    phone = Column(String(20), nullable=True)
    address = Column(String(300), nullable=True)
    order_type = Column(String(20), nullable=False)
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))

    #Tracking System
    order_details = relationship("OrderDetail", back_populates="order")
    tracking_id = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    status = Column(String(50), default="Pending")