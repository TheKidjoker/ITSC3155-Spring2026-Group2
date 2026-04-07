from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import order_tracking as controller
from ..schemas import orders as order_schema
from ..schemas import order_tracking as tracking_schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Order Tracking"],
    prefix="/tracking",
)


@router.get("/{tracking_id}", response_model=order_schema.Order)
def get_order_by_tracking_id(tracking_id: str, db: Session = Depends(get_db)):
    return controller.get_by_tracking_id(db, tracking_id)


@router.patch("/{tracking_id}/status", response_model=order_schema.Order)
def update_order_status(
    tracking_id: str,
    body: tracking_schema.OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    return controller.update_status(db, tracking_id, body)
