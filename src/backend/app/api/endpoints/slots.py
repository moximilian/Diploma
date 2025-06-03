"""
Logic to work with API
"""

from fastapi import APIRouter, Depends

import schemas
from crud.slots import SlotsCRUD
from crud.auth import authorised_user
from database import get_db
router = APIRouter()


@router.post('/slots/create', response_model=None)
async def create_slot(item: schemas.SlotInsertIn, db=Depends(get_db), user=Depends(authorised_user)):
    controller = SlotsCRUD(db, user)
    return controller.create_slot(item)


@router.post('/slots/get', response_model=schemas.SlotModelOut)
async def get_item(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = SlotsCRUD(db, user)
    recieved_item = controller.get(item)
    return recieved_item


@router.post('/slots/list', response_model=schemas.BaseListResponse)
async def get_list(item: schemas.RequestBodyList, db=Depends(get_db), user=Depends(authorised_user)):
    controller = SlotsCRUD(db, user)
    return controller.list(item)

@router.post('/slots/enter')
async def get_list(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = SlotsCRUD(db, user)
    return controller.enter(item)

@router.post('/slots/leave')
async def get_list(body: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = SlotsCRUD(db, user)
    return controller.leave(body)


@router.post('/slots/update', response_model=schemas.SlotModelOut)
async def update(item: schemas.SlotModel, db=Depends(get_db), user=Depends(authorised_user)):
    controller = SlotsCRUD(db, user)
    return controller.update(item)


@router.post('/slots/delete', response_model=schemas.SlotModelOut)
async def delete(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = SlotsCRUD(db, user)
    return controller.delete(item)

