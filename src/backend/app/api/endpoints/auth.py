"""
Authorization logic
"""

from fastapi import APIRouter, Depends

import schemas
from crud.auth import Authorisation
from database import get_db
router = APIRouter()


@router.post('/auth/register', response_model=schemas.UserOut)
async def register(body: schemas.UserCreate, db=Depends(get_db)):
    controller = Authorisation(db)
    return controller.register(body)


@router.post('/auth/login', response_model=schemas.Token)
async def login(body: schemas.UserLogin, db=Depends(get_db)):
    controller = Authorisation(db)
    return controller.authorize(body)


@router.post('/auth/logout', response_model=schemas.AuthSession)
async def logout(body: schemas.BaseItemIn, db=Depends(get_db)):
    controller = Authorisation(db)
    return controller.logout(body)
