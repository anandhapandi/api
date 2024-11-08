from fastapi import FastAPI, HTTPException
from typing import List 
from app.schemas import ItemCreate, ItemResponse
from app.crud import get_items, get_item, create_item, update_item, delete_item

app = FastAPI()

@app.get("/items/", response_model=List[ItemResponse])
def read_items():
    return get_items()

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=ItemResponse)
def create_new_item(item: ItemCreate):
    return create_item(item)

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_existing_item(item_id: int, item: ItemCreate):
    updated_item = update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}", response_model=bool)
def delete_existing_item(item_id: int):
    if not delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return True
