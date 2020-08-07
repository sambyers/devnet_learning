from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    ip: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "devnet example api"}


@app.get("/inventory/{item}")
async def get_inventory(item: str):
    return {"item": item}


@app.post("/inventory/")
async def add_inventory(item: Item):
    if item.description:
        return {"created": item}
    else:
        item.description = f'{item.name} - {item.ip}'
        return {"created": item}
