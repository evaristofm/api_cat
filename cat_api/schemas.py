from typing import List, Optional

from pydantic import BaseModel



class CatIn(BaseModel):
    breed: str
    location_origin: str
    coat_length: str
    body_type: str
    pattern: str

class Cat(CatIn):
    id: int

    class Config:
        orm_mode = True
    