from app.models import fake_db, Item
from app.schemas import ItemCreate, ItemResponse
from typing import List, Optional

def get_items() -> List[ItemResponse]:
    """ Get all items """
    return [ItemResponse(id=index, **item.dict()) for index, item in enumerate(fake_db)]

def get_item(item_id: int) -> Optional[ItemResponse]:
    """ Get a single item by ID """
    if item_id < len(fake_db):
        item = fake_db[item_id]
        return ItemResponse(id=item_id, **item.dict())
    return None

def create_item(item: ItemCreate) -> ItemResponse:
    """ Create a new item """
    new_item = Item(**item.dict())
    fake_db.append(new_item)
    return ItemResponse(id=len(fake_db) - 1, **new_item.dict())

def update_item(item_id: int, item: ItemCreate) -> Optional[ItemResponse]:
    """ Update an existing item """
    if item_id < len(fake_db):
        fake_db[item_id] = Item(**item.dict())
        return ItemResponse(id=item_id, **fake_db[item_id].dict())
    return None

def delete_item(item_id: int) -> bool:
    """ Delete an item by ID """
    if item_id < len(fake_db):
        del fake_db[item_id]
        return True
    return False
