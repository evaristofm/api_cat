from typing import List
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

some_dict = dict(
    path1="AcceptedEventRelation",
    path2="Account",
    path3="AccountChangeEvent",
    path4="AccountCleanInfo",
    path5="AccountContactRole"
)

Subjects = Enum('Subjects', some_dict)


@app.get("/cats", response_model=List[schemas.Cat])
def cats_list(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    cat_db = crud.get_cats(db=db, skip=skip, limit=limit)
    return cat_db

@app.post("/cats", response_model=schemas.Cat)
def cat_create(cat: schemas.CatIn, db: Session = Depends(get_db)):
    return crud.create_cat(db=db, cat=cat)

 