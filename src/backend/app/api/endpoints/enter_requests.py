"""
Logic to work with API
"""

from fastapi import APIRouter, Depends

import schemas
from crud.enter_requests import EnterRequestsCRUD
from crud.auth import authorised_user
from database import get_db
router = APIRouter()


@router.post('/groups/requests/create', response_model=schemas.EnterRequestOut)
async def create_enter_request(item: schemas.BaseEnterRequestCreate, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EnterRequestsCRUD(db, user)
    return controller.create_enter_request(item)

@router.post('/groups/requests/approve', response_model=schemas.EnterRequestOut)
async def create_enter_request(item: schemas.EnterRequestUpdate, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EnterRequestsCRUD(db, user)
    return controller.approve_request(item)

@router.post('/groups/requests/revoke', response_model=schemas.EnterRequestOut)
async def create_enter_request(item: schemas.EnterRequestUpdate, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EnterRequestsCRUD(db, user)
    return controller.revoke_request(item)


@router.post('/groups/requests/list', response_model=schemas.BaseListResponse)
async def read_items(request_body: schemas.RequestBodyList, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EnterRequestsCRUD(db, user)
    return controller.read_items(request_body)

@router.post('/groups/requests/delete', response_model=schemas.EnterRequestOut)
async def read_items(request_body: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EnterRequestsCRUD(db, user)
    return controller.delete_request(request_body)
