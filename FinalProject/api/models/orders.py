from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
import uuid


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
<<<<<<< HEAD
    customer_name = Column(String(100))
=======
    user_id = Column(Integer, nullable=True)

    #Guest detailds
    customer_name = Column(String(100))
    phone = Column(String(20), nullable=True)
    address = Column(String(300), nullable=True)
    order_type = Column(String(20), nullable=False)
>>>>>>> origin/main
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))

    order_details = relationship("OrderDetail", back_populates="order")
<<<<<<< HEAD

    #Tracking System
    tracking_id = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    order_status = Column(String(50), nullable=False, server_default="Pending")
=======
    tracking_id = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    status = Column(String(50), default="Pending")
>>>>>>> origin/main
