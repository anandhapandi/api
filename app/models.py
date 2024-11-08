from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

fake_db: List[Item] = []
