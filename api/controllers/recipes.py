from ..models import recipes as recipe_model
from ..schemas import recipes as recipe_schema

def create(db: Session, recipe):
    # Create a new instance of the Recipe model with the provided data
    db_recipe = recipe_model.Recipe(**recipe.model_dump())
    # Add the newly created Recipe object to the database session
    db.add(db_recipe)
    # Commit the changes to the database
    db.commit()
    # Refresh the Recipe object to ensure it reflects the current state in the database
    db.refresh(db_recipe)
    # Return the newly created Recipe object
    return db_recipe


def read_all(db: Session):
    return db.query(recipe_model.Recipe).all()


def read_one(db: Session, recipe_id):
    return db.query(recipe_model.Recipe).filter(recipe_model.Recipe.id == recipe_id).first()


def update(db: Session, recipe_id, recipe):
    # Query the database for the specific recipe to update
    db_recipe = db.query(recipe_model.Recipe).filter(recipe_model.Recipe.id == recipe_id)
    # Extract the update data from the provided 'recipe' object
    update_data = recipe.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_recipe.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated recipe record
    return db_recipe.first()


def delete(db: Session, recipe_id):
    # Query the database for the specific recipe to delete
    db_recipe = db.query(recipe_model.Recipe).filter(recipe_model.Recipe.id == recipe_id)
    # Delete the database record without synchronizing the session
    db_recipe.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)