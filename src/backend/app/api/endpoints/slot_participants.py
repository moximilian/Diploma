"""
Logic to work with API
"""

from fastapi import APIRouter, Depends

import schemas
import models as m
from crud.base import BaseCRUD
from crud.auth import authorised_user
from database import get_db
router = APIRouter()


@router.post('/slot_participans/update')
async def update(item:schemas.SlotParticipantModel, db=Depends(get_db), user=Depends(authorised_user)):
    controller = BaseCRUD(db, m.SlotParticipant)
    user
    return controller.update(item)


# @router.post('/slot_participans/delete')
# async def delete_group_participant(item:schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
#     controller = SlotParticipantCURD(db, user)
#     return controller.delete(item)


@router.post('/slot_participans/list', response_model=schemas.BaseListResponse)
async def list(item:schemas.RequestBodyList, db=Depends(get_db), user=Depends(authorised_user)):
    controller = BaseCRUD(db, m.SlotParticipant)
    user
    return controller.list(item)
