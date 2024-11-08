from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemResponse(ItemCreate):
    id: int  
