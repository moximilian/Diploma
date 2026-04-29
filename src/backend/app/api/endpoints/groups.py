"""
Logic to work with API
"""

from fastapi import APIRouter, Depends

import schemas
from crud.groups import GroupsCRUD
from crud.auth import authorised_user
from database import get_db
router = APIRouter()


@router.post('/groups/create', response_model=None)
async def create_group(item: schemas.GroupBase, db=Depends(get_db), user=Depends(authorised_user)):
    controller = GroupsCRUD(db, user)
    return controller.create_group(item)


@router.post('/groups/get', response_model=schemas.GroupOut)
async def get_item(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = GroupsCRUD(db, user)
    return controller.get(item)


@router.post('/groups/list', response_model=schemas.BaseListResponse)
async def get_list(item: schemas.RequestBodyList, db=Depends(get_db), user=Depends(authorised_user)):
    controller = GroupsCRUD(db, user)
    return controller.list(item)


@router.post('/groups/update', response_model=schemas.GroupOut)
async def update(item: schemas.GroupUpdateIn, db=Depends(get_db), user=Depends(authorised_user)):
    controller = GroupsCRUD(db, user)
    return controller.update(item)


@router.post('/groups/delete', response_model=schemas.GroupOut)
async def delete(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = GroupsCRUD(db, user)
    return controller.mark_deleted(item)


@router.post('/groups/enter', response_model=schemas.GroupOut)
async def enter_group(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = GroupsCRUD(db, user)
    return controller.enter_group(item)


@router.post('/groups/leave', response_model=dict)
async def leave_group(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = GroupsCRUD(db, user)
    return controller.leave_group(item)
