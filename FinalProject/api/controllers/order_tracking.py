from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import orders as model
from ..schemas import order_tracking as schemas


def get_by_tracking_id(db: Session, tracking_id: str):
    try:
        order = (
            db.query(model.Order)
            .filter(model.Order.tracking_id == tracking_id)
            .first()
        )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tracking id not found",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def update_status(db: Session, tracking_id: str, body: schemas.OrderStatusUpdate):
    try:
        order = (
            db.query(model.Order)
            .filter(model.Order.tracking_id == tracking_id)
            .first()
        )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tracking id not found",
            )
        order.order_status = body.order_status
        db.commit()
        db.refresh(order)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order
