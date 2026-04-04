#logic for menu items

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import menu_items as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    #New MenuItem object from request data
    new_item = model.MenuItem(
        item_name = request.item_name,
        price = request.price,
        calories = request.calories,
        food_category = request.food_category,
        description = request.description
    )

    try:
        db.add(new_item) #stage new item object
        db.commit() # save to db
        db.refresh(new_item) #reload db to get id
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error) # throw an error code if db fails

    return new_item

def read_all(db: Session):
    #return all items in db
    try:
        result = db.query(model.MenuItem).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error) # throw an error code if db fails
    return result

def read_by_category(db: Session, category: str):
    #return menu items by category
    try:
        result = db.query(model.MenuItem).filter(model.MenuItem.food_category == category).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error) # throw an error code if db fails
    return result

def read_one(db: Session, item_id):
    #return one menu item by id
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error) # throw an error code if db fails
    return item

def update(db: Session, item_id, request):
    #update menu item by id
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error) # throw an error code if db fails
    

def delete(db: Session, item_id):
    #delete menu item by id
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error) # throw an error code if db fails
    return Response(status_code=status.HTTP_204_NO_CONTENT)