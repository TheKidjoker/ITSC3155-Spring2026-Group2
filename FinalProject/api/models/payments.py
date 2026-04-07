from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from datetime import datetime

from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    method = Column(String(50), nullable=False, server_default="card")
    status = Column(String(50), nullable=False, server_default="pending")
    created_at = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
