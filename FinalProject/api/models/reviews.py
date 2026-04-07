from sqlalchemy import Column, ForeignKey, Integer, String

from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=True)
    customer_name = Column(String(100), nullable=True)
