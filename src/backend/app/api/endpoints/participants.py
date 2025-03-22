"""
Logic to work with API
"""

from fastapi import APIRouter, Depends

import schemas
from crud.participants import ParticipantsCRUD
from crud.base import BaseCRUD
import models as m

from crud.auth import authorised_user
from database import get_db
router = APIRouter()



@router.post('/participants/list', response_model=schemas.BaseListResponse)
async def get_list(item: schemas.RequestBodyList, db=Depends(get_db), user=Depends(authorised_user)):
    controller = ParticipantsCRUD(db, user)
    return controller.list(item)


@router.post('/participants/delete', response_model=None)
async def delete_items(items: schemas.RequestBodyOnes, db=Depends(get_db), user=Depends(authorised_user)):
    controller = BaseCRUD(db, m.Participant)
    return controller.delete(items)

@router.post('/participants/get', response_model=schemas.Participant)
async def get_item(item: schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = BaseCRUD(db, m.Participant)
    return controller.get(item)
