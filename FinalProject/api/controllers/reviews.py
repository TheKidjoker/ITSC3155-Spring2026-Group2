from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError

from ..models import reviews as model
from ..models import sandwiches as sandwich_model
from ..schemas import reviews as schemas


def create(db: Session, request: schemas.ReviewCreate):
    if request.sandwich_id is not None:
        sw = (
            db.query(sandwich_model.Sandwich)
            .filter(sandwich_model.Sandwich.id == request.sandwich_id)
            .first()
        )
        if not sw:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich id not found"
            )

    new_item = model.Review(
        sandwich_id=request.sandwich_id,
        rating=request.rating,
        comment=request.comment,
        customer_name=request.customer_name,
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item


def read_all(db: Session):
    try:
        return db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Review).filter(model.Review.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id: int, request: schemas.ReviewUpdate):
    try:
        q = db.query(model.Review).filter(model.Review.id == item_id)
        if not q.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        update_data = request.dict(exclude_unset=True)
        if update_data.get("sandwich_id") is not None:
            sw = (
                db.query(sandwich_model.Sandwich)
                .filter(
                    sandwich_model.Sandwich.id == update_data["sandwich_id"]
                )
                .first()
            )
            if not sw:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sandwich id not found",
                )
        q.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return q.first()


def delete(db: Session, item_id: int):
    try:
        q = db.query(model.Review).filter(model.Review.id == item_id)
        if not q.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        q.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
