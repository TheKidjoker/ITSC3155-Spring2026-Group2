from ..models import resources as resource_model
from ..schemas import resources as resource_schema


def create(db: Session, resource):
    # Create a new instance of the Resource model with the provided data
    db_resource = resource_model.Resource(**resource.model_dump())
    # Add the newly created Resource object to the database session
    db.add(db_resource)
    # Commit the changes to the database
    db.commit()
    # Refresh the Resource object to ensure it reflects the current state in the database
    db.refresh(db_resource)
    # Return the newly created Resource object
    return db_resource


def read_all(db: Session):
    return db.query(resource_model.Resource).all()


def read_one(db: Session, resource_id):
    return db.query(resource_model.Resource).filter(resource_model.Resource.id == resource_id).first()


def update(db: Session, resource_id, resource):
    # Query the database for the specific resource to update
    db_resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == resource_id)
    # Extract the update data from the provided 'resource' object
    update_data = resource.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_resource.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated resource record
    return db_resource.first()


def delete(db: Session, resource_id):
    # Query the database for the specific resource to delete
    db_resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == resource_id)
    # Delete the database record without synchronizing the session
    db_resource.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)