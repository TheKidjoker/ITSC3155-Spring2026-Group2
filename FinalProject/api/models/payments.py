from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    payment_type = Column(String(50), nullable=False)
    transaction_status = Column(String(50), nullable=False, server_default="pending")
    card_number = Column(String(4), nullable=True)
    payment_amount = Column(DECIMAL(8, 2), nullable=False, server_default='0.0')
    payment_date = Column(DATETIME, nullable=False, server_default=func.now())

    order = relationship("Order", back_populates="payment")
