"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models as m
from crud.base import BaseCRUD
from schemas import GroupOut, RequestBodyOne, EventInsertIn
import api.exceptions as exc


class EventsCRUD(BaseCRUD):
    """CRUD logic to work with events.
     """

    def __init__(self, db: Session, auth_user):
        """ Initialize class.

            Args:
                db (Session): DB session
                auth_user (models.User): User that performs actions in this crud
            """
        super().__init__(db, m.Event)
        self.user = auth_user        
