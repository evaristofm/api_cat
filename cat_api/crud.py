from sqlalchemy.orm import Session

from . import models, schemas


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

