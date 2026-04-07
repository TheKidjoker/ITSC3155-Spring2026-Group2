from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError

from ..models import recipes as model
from ..models import sandwiches as sandwich_model
from ..models import resources as resource_model
from ..schemas import recipes as schemas


def create(db: Session, request: schemas.RecipeCreate):
    sw = (
        db.query(sandwich_model.Sandwich)
        .filter(sandwich_model.Sandwich.id == request.sandwich_id)
        .first()
    )
    if not sw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich id not found"
        )
    res = (
        db.query(resource_model.Resource)
        .filter(resource_model.Resource.id == request.resource_id)
        .first()
    )
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource id not found"
        )

    new_item = model.Recipe(
        sandwich_id=request.sandwich_id,
        resource_id=request.resource_id,
        amount=request.amount,
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
        return db.query(model.Recipe).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Recipe).filter(model.Recipe.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id: int, request: schemas.RecipeUpdate):
    try:
        q = db.query(model.Recipe).filter(model.Recipe.id == item_id)
        if not q.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        update_data = request.dict(exclude_unset=True)
        if "sandwich_id" in update_data:
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
        if "resource_id" in update_data:
            res = (
                db.query(resource_model.Resource)
                .filter(
                    resource_model.Resource.id == update_data["resource_id"]
                )
                .first()
            )
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Resource id not found",
                )
        q.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return q.first()


def delete(db: Session, item_id: int):
    try:
        q = db.query(model.Recipe).filter(model.Recipe.id == item_id)
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
