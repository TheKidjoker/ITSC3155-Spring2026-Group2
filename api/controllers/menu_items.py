from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.menu_item import MenuItem
from ..schemas.menu_item import MenuItemResponse

router = APIRouter()  # ✅ THIS WAS MISSING

@router.get("/menu-items/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item