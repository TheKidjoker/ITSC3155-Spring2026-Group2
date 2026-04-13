from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_percentage = Column(DECIMAL(5, 2), nullable=True)
    discount_amount = Column(DECIMAL(8, 2), nullable=True)
    expiration_date = Column(DATETIME, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")

    orders = relationship("Order", back_populates="promotion")
