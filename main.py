from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Item, ItemCreate, ItemResponse
from database import AsyncSessionLocal, engine, Base  
from fastapi.responses import JSONResponse
from fastapi import Request

app = FastAPI()

# Dependency for database session
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    # Create the database tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = Item(name=item.name)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[ItemResponse])
async def read_items(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).offset(skip).limit(limit))
    items = result.scalars().all()
    return items

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    db_item = result.scalars().first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    await db.commit()
    await db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    db_item = result.scalars().first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(db_item)
    await db.commit()
    return {"detail": "Item deleted"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

