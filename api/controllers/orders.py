from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import order_details as od_model
from ..models import sandwiches as sandwich_model
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from ..schemas import orders as schemas
from datetime import datetime, date


def create(db: Session, request):
    if request.order_type not in ("delivery", "takeout"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order_type must be 'delivery' or 'takeout'"
        )

    if request.order_type == "delivery" and not request.address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="address is required for delivery orders"
        )

    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        order_type=request.order_type,
        address=request.address
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def read_by_tracking_id(db: Session, tracking_id: str):
    try:
        item = db.query(model.Order).filter(model.Order.tracking_id == tracking_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_all_by_date_range(db: Session, start_date: date, end_date: date):
    try:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())
        result = db.query(model.Order).filter(
            model.Order.order_date >= start_dt,
            model.Order.order_date <= end_dt
        ).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def get_revenue(db: Session, revenue_date: date):
    try:
        start_dt = datetime.combine(revenue_date, datetime.min.time())
        end_dt = datetime.combine(revenue_date, datetime.max.time())
        result = db.query(
            func.sum(sandwich_model.Sandwich.price * od_model.OrderDetail.amount)
        ).join(
            od_model.OrderDetail, model.Order.id == od_model.OrderDetail.order_id
        ).join(
            sandwich_model.Sandwich, od_model.OrderDetail.sandwich_id == sandwich_model.Sandwich.id
        ).filter(
            model.Order.order_date >= start_dt,
            model.Order.order_date <= end_dt
        ).scalar()

        return {"date": str(revenue_date), "total_revenue": float(result) if result else 0.0}
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def guest_order(db: Session, order: schemas.GuestOrder):
    db_order = model.Order(
        customer_name = order.customer_name,
        phone = order.phone,
        address = order.address
        #sandwich_id
    )
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    except SQLAlchemyError as e:
        db.rollback() # Always rollback on failure
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
