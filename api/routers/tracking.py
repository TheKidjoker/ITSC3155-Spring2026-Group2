from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Order Tracking'],
    prefix="/orders/tracking"
)


@router.get("/{tracking_id}", response_model=schema.Order)
def get_order_by_tracking_id(tracking_id: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking_id(db, tracking_id)
