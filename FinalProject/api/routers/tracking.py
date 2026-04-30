from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Tracking'],
    prefix="/tracking"
)


@router.get("/{tracking_id}", response_model=schema.Order)
def track_order(tracking_id: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking(db, tracking_id=tracking_id)
