from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

#imports to get data from database
from ..controllers import recipes, sandwiches
from ..dependencies.database import get_db

#access to database session
router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/")
def get_menu(db: Session = Depends(get_db)):
    all_recipes = recipes.read_all(db) #get all recipes from database
    all_sandiwches = sandwiches.read_all(db) #get all sandwiches from database

    #return both recipes and sandwiches as one response
    #frontend can call /menu to get everything in one sweep.
    return{
        'recipes': all_recipes,
        'sandwiches': all_sandiwches
    }
