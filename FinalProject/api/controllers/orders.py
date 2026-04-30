from datetime import date
from sqlalchemy import func, cast, Date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError
from ..schemas import orders as schemas


def create(db: Session, request):
    if request.order_type.lower() not in ("delivery", "takeout", "pickup"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order_type must be 'delivery', 'takeout', or 'pickup'"
        )

    if request.order_type.lower() == "delivery" and not request.address:
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

def read_by_tracking(db: Session, tracking_id: str):
    try:
        item = db.query(model.Order).filter(model.Order.tracking_id == tracking_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_by_date_range(db: Session, start_date: date, end_date: date):
    try:
        result = db.query(model.Order).filter(
            cast(model.Order.order_date, Date) >= start_date,
            cast(model.Order.order_date, Date) <= end_date
        ).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def get_revenue(db: Session, revenue_date: date):
    try:
        result = db.query(
            func.sum(model.Order.total_price)
        ).filter(
            cast(model.Order.order_date, Date) == revenue_date
        ).scalar()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {"date": str(revenue_date), "total_revenue": float(result) if result else 0.0}


def guest_order(db: Session, order: schemas.GuestOrder):
    from ..models import order_details as od_model

    db_order = model.Order(
        customer_name=order.customer_name,
        phone=order.phone,
        address=order.address,
        order_type="delivery",
        description="Guest order"
    )
    try:
        db.add(db_order)
        db.flush()

        db_detail = od_model.OrderDetail(
            order_id=db_order.id,
            sandwich_id=order.sandwich_id,
            amount=order.quantity
        )
        db.add(db_detail)
        db.commit()
        db.refresh(db_order)
        return db_order
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
