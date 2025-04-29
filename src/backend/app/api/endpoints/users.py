"""
Users logic
"""

from fastapi import APIRouter, Depends

import schemas
from crud.users import User
from crud.auth import authorised_user

from database import get_db
router = APIRouter()


@router.post('/user/change_password', response_model=schemas.UserOut)
async def change_password(body: schemas.PasswordsChange, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = User(db, current_user)
    return controller.change_password(body)


@router.post('/user/get', response_model=schemas.UserOut)
async def get_user(body: schemas.RequestBodyOne, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = User(db, current_user)
    return controller.get(body)

@router.post('/user/list', response_model=schemas.BaseListResponse)
async def get_user(body: schemas.RequestBodyList, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = User(db, current_user)
    return controller.list(body)


@router.post('/user/update', response_model=schemas.UserOut)
async def update_user(body: schemas.UserInUpdate, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = User(db, current_user)
    return controller.update(body)


@router.post('/user/delete', response_model=schemas.UserOut)
async def delete_user(body: schemas.RequestBodyOne, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = User(db, current_user)
    return controller.mark_deleted(body)
