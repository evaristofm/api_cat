from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    breed = Column(String, index=True)
    location_origin = Column(String, index=True)
    coat_length = Column(String, index=True)
    body_type = Column(String, index=True)
    pattern = Column(String, index=True)

