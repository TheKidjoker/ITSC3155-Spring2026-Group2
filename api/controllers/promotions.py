from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import promotions as model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def create(db: Session, request):
    new_item = model.Promotion(
        code=request.code,
        discount_percentage=request.discount_percentage,
        discount_amount=request.discount_amount,
        expiration_date=request.expiration_date,
        is_active=request.is_active
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
        result = db.query(model.Promotion).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Promotion).filter(model.Promotion.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Promotion).filter(model.Promotion.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.model_dump(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Promotion).filter(model.Promotion.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def apply_promo_code(db: Session, request):
    try:
        promo = db.query(model.Promotion).filter(model.Promotion.code == request.code).first()
        if not promo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")

        if not promo.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promo code is no longer active.")

        if promo.expiration_date and promo.expiration_date < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promo code has expired.")

        new_total = request.order_total
        discount_percentage = float(promo.discount_percentage) if promo.discount_percentage else None
        discount_amount = float(promo.discount_amount) if promo.discount_amount else None

        if discount_percentage:
            new_total -= new_total * (discount_percentage / 100)
        if discount_amount:
            new_total -= discount_amount

        if new_total < 0:
            new_total = 0

        return {
            "code": promo.code,
            "discount_percentage": discount_percentage,
            "discount_amount": discount_amount,
            "new_total": round(new_total, 2)
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
