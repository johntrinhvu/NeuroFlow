from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models import Item

router = APIRouter()

@router.get("/items/", response_model=list[Item])
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items

@router.post("/items/", response_model=Item)
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
