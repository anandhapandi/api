from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Pydantic models for validation
class ItemCreate(BaseModel):
    name: str

class ItemResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

