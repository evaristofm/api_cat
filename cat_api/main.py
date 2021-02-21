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


@app.get("/cats/", response_model=List[schemas.Cat])
def list_cats(breed: str = None, location: str = None, coat: str = None, body: str = None, pattern: str = None, db: Session = Depends(get_db)):
    cats = crud.get_cats_with_filter(db=db, breed=breed, location=location, coat=coat, body=body, pattern=pattern)
    return cats

@app.get("/cats", response_model=List[schemas.Cat])
def cats_all(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    cats_db = crud.get_cats(db=db, skip=skip, limit=limit)
    return cats_db

@app.get("/cats/{id}", response_model=schemas.Cat)
def cats_one(id: int, db: Session = Depends(get_db)):
   cat = crud.get_cat(db=db, cat_id=id)
   if cat is None:
       raise HTTPException(404, detail="Cat Not Found")
   return cat

@app.post("/cats", response_model=schemas.Cat)
def cat_create(cat: schemas.CatIn, db: Session = Depends(get_db)):
    return crud.create_cat(db=db, cat=cat)

@app.put("/cats/{id}", response_model=schemas.Cat)
def update_cat(cat: schemas.CatIn, id: int, db: Session = Depends(get_db)):
    cat = crud.update_cat(db=db, id=id, cat=cat)
    if cat is None:
        raise HTTPException(404, detail="Cat Not Found.")
    return cat

@app.delete("/cats/{id}")
def delete_cat(id: int, db: Session = Depends(get_db)):
    cat = crud.get_cat(db=db, cat_id=id)
    if cat:
        crud.delete_cat(db=db, id=id)
        return {"message": "Cat Deleted"}
    raise HTTPException(404, detail="Cat Not Found")
