"""
Logic to work with API
"""

from fastapi import APIRouter, Depends

import schemas
from crud.events import EventsCRUD
from crud.auth import authorised_user
from database import get_db
router = APIRouter()


@router.post('/events/create', response_model=None)
async def create_event(item: schemas.EventInsertIn, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventsCRUD(db, user)
    return controller.create_event(item)


@router.post('/events/get', response_model=schemas.EventModel)
async def get_item(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventsCRUD(db, user)
    return controller.get(item)


@router.post('/events/list', response_model=schemas.BaseListResponse)
async def get_list(item: schemas.RequestBodyList, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventsCRUD(db, user)
    return controller.list(item)


@router.post('/events/update', response_model=schemas.EventModel)
async def update(item: schemas.EventInsertIn, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventsCRUD(db, user)
    return controller.update(item)


@router.post('/events/delete', response_model=schemas.EventModel)
async def delete(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventsCRUD(db, user)
    return controller.mark_deleted(item)

