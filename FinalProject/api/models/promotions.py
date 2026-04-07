from sqlalchemy import Boolean, Column, Integer, String

from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_percent = Column(Integer, nullable=False)
    description = Column(String(300), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
