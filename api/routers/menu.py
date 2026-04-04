# API endpoints for items in menu

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional



from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..dependencies.database import engine, get_db

#routes start with /menu
router = APIRouter(prefix='/menu', tags=["Menu"])

#return items by category
@router.get("/", response_model=list[schema.MenuItem])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

#return one specific item by category
@router.get("/search", response_model=list[schema.MenuItem])
def search_by_category(category: str, db: Session = Depends(get_db)):
    return controller.read_by_category(db, category)

#return one specific item by id
@router.get("/{item_id}", response_model=schema.MenuItem)
def get_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)

#staff can create a new item
@router.post("/", response_model=schema.MenuItem)
def create(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

#staff can update an existing item
@router.put("/{item_id}", response_model=schema.MenuItem)
def update(item_id: int, request: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)

#staff can delete items
@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)
