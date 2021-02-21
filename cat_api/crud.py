from sqlalchemy.orm import Session

from . import models, schemas


def get_cats_with_filter(
    db: Session, breed: str = None, location: str = None,
    coat: str = None, body: str = None, pattern: str = None
):
    if breed:
        return db.query(models.Cat).filter(models.Cat.breed == breed).all()
    elif location:
        return db.query(models.Cat).filter(models.Cat.location_origin == location).all()
    elif coat:
        return db.query(models.Cat).filter(models.Cat.coat_length == coat).all()
    elif body:
        return db.query(models.Cat).filter(models.Cat.body_type == body).all()
    elif pattern:
        return db.query(models.Cat).filter(models.Cat.pattern == pattern).all()
    return db.query(models.Cat).all()


def get_cat(db: Session, cat_id: int):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()

def get_cats(db: Session, skip: int, limit: int):
    return db.query(models.Cat).offset(skip).limit(limit).all()

def create_cat(db: Session, cat: schemas.Cat):
    cat_db = models.Cat(**cat.dict())
    db.add(cat_db)
    db.commit()
    db.refresh(cat_db)
    return cat_db

def update_cat(db: Session, id: int, cat: schemas.Cat):
    cat_db = get_cat(db=db, cat_id=id)

    cat_db.breed = cat.breed if cat.breed != 'string' else cat_db.breed
    cat_db.location_origin = cat.location_origin if cat.location_origin != 'string' else cat_db.location_origin
    cat_db.coat_length = cat.coat_length if cat.coat_length != 'string' else cat_db.coat_length
    cat_db.body_type = cat.body_type if cat.body_type != 'string' else cat_db.body_type
    cat_db.pattern = cat.pattern if cat.pattern != 'string' else cat_db.pattern

    db.commit()
    db.refresh(cat_db)
    return cat_db

def delete_cat(db: Session, id: int):
    db.query(models.Cat).filter(models.Cat.id == id).delete()
    db.commit()
    