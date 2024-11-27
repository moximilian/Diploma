"""
Users logic
"""

from fastapi import APIRouter, Depends

import schemas
from crud.auth import User, authorised_user

from database import get_db
router = APIRouter()


@router.post('/user/change_password', response_model=schemas.UserOut)
async def change_password(body: schemas.PasswordsChange, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = User(db, current_user)
    return controller.change_password(body)

@router.post('/user/get', response_model=schemas.UserOut)
async def change_password(body: schemas.RequestBodyOne, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = User(db, current_user)
    return controller.get(body)

@router.post('/user/delete', response_model=schemas.UserOut)
async def change_password(body: schemas.RequestBodyOne, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = User(db, current_user)
    return controller.mark_deleted(body)

