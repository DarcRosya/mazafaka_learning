from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

items = {}

@app.get("/")
def read_root():
    return {"message": "hello guyyyyys :3"}

@app.get("/items")
def get_items():
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    item = items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": item, "q": q}

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in items:
        raise HTTPException(status_code=409, detail="Item already exists")
    items[item_id] = item
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        return {"error": "Item not found"}
    items[item_id] = item
    return item