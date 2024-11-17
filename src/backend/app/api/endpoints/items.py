"""
Logic to work with API
"""

from fastapi import APIRouter, Depends

import schemas
from crud.items import ItemsCRUD
from database import get_db
router = APIRouter()

@router.post('/items/insert', response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db=Depends(get_db)):
    controller = ItemsCRUD(db)
    return controller.create_item(item)

@router.post('/items/list', response_model=list[schemas.Item])
async def read_items(request_body: dict, db=Depends(get_db)):
    controller = ItemsCRUD(db)
    return controller.read_items(request_body)
