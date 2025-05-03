"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
import models as m
from crud.base import BaseCRUD
from crud.users import User


class ParticipantsCRUD(BaseCRUD):
    """CRUD logic to work with participants.
    """

    def __init__(self, db: Session, auth_user):
        """ Initialize class.

        Args:
            db (Session): DB session
            auth_user (models.User): User that performs actions in this crud
        """
        super().__init__(db, m.Participant)
        self.user = auth_user
        self.userCRUD = User(db, auth_user)

    def list(self, body):
        rows = super().get_items(body)

        result_rows = []
        for row in rows:
            participant = self.userCRUD.get({'id': row.user_id}).dict()
            participant.pop('password', {})
            participant['group_id'] = row.group_id
            participant['user_id'] = row.user_id
            participant['has_events'] = len(row.events) != 0
            participant['id'] = row.id
            result_rows.append(participant)
        return super()._transform_response(result_rows)
