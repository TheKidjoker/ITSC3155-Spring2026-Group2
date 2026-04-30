from datetime import date
from fastapi import APIRouter, Depends, FastAPI, status, Response, Query
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/date-range", response_model=list[schema.Order])
def read_by_date_range(start_date: date = Query(...), end_date: date = Query(...), db: Session = Depends(get_db)):
    return controller.read_by_date_range(db, start_date=start_date, end_date=end_date)


@router.get("/revenue")
def get_revenue(revenue_date: date = Query(...), db: Session = Depends(get_db)):
    return controller.get_revenue(db, revenue_date=revenue_date)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.post("/guest", response_model=schema.Order)
def checkout_as_guest(order: schema.GuestOrder, db: Session = Depends(get_db)):
    return controller.guest_order(db=db, order=order)
