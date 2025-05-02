"""
Logic to work with API
"""

from fastapi import APIRouter, Depends

import schemas
from crud.event_participans import EventParticipansCRUD
from crud.auth import authorised_user
from database import get_db
router = APIRouter()

@router.post('/event_participans/add_one')
async def add_group_participant(item, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventParticipansCRUD(db, user)
    return controller.add_one_participant(item)

@router.post('/event_participans/update')
async def add_group_participant(item:schemas.EventParticipantModel, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventParticipansCRUD(db, user)
    return controller.update(item)

@router.post('/event_participans/add_all')
async def add_all_group_participants(item:schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventParticipansCRUD(db, user)
    return controller.add_all_group_participants(item)

@router.post('/event_participans/delete')
async def delete_group_participant(item:schemas.RequestBodyOne, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventParticipansCRUD(db, user)
    return controller.delete(item)


@router.post('/event_participans/list', response_model=schemas.BaseListResponse)
async def delete_group_participant(item:schemas.RequestBodyList, db=Depends(get_db), user=Depends(authorised_user)):
    controller = EventParticipansCRUD(db, user)
    return controller.list(item)
