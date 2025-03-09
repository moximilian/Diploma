"""
Images logic
"""

from fastapi import APIRouter, Depends

import schemas
from crud.images import Image
from crud.auth import authorised_user

from database import get_db
router = APIRouter()

@router.post('/images/set_user', response_model=schemas.ImageInOut)
async def update_profile_pic(body: schemas.ImageCreate, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = Image(db, current_user)
    return controller.update_profile_pic(body)

@router.post('/images/get', response_model=schemas.ImageInOut)
async def get_profile_pic(body: schemas.RequestBodyOne, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = Image(db, current_user)
    return controller.get_image(body)


@router.post('/images/delete_user', response_model=None)
async def delete_profile_pic(body: schemas.RequestBodyOne, db=Depends(get_db), current_user=Depends(authorised_user)):
    controller = Image(db, current_user)
    return controller.delete_profile_pic(body)