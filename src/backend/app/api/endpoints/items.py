"""
Logic to work with API
"""

from fastapi import APIRouter

import app.schemas as schemas
from backend.app.crud.items import ItemsCRUD
from backend.app.api.api import db
router = APIRouter()

@router.post('/items/insert', response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate):
    return ItemsCRUD(db).create_item(item)

@router.post('/items/read', response_model=list[schemas.Item])
async def read_items(request_body):
    return ItemsCRUD(db).read_items(request_body)