"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_

import models as m
from crud.base import BaseCRUD
from schemas import GroupOut, RequestBodyOne
import api.exceptions as exc


class GroupsCRUD(BaseCRUD):
    """CRUD logic to work with groups.
    """

    def __init__(self, db: Session, auth_user: GroupOut):
        """ Initialize class.

        Args:
            db (Session): DB session
            auth_user (models.User): User that performs actions in this crud
        """
        super().__init__(db, m.Group)
        self.user = auth_user

    def create_group(self, item: GroupOut) -> m.Group:
        """ Create group based on given parametres.

        Args:
            item (GroupOut): Parametres for new group to create

        Returns:
            models.Group: new created group with ID
        """
        new_group = self.model(
            creator_id=self.user.get('id'),
            name=item.get('name', ''),
            description=item.get('description', ''),
            is_open=item.get('is_open', True),
            max_participants_count=item.get('max_participants_count', 1),
            is_deleted=item.get('is_deleted', False),
        )
        new_group = self._save_to_db(new_group)
        return new_group

    def enter_group(self, body: RequestBodyOne) -> m.Group:
        """Enter someone's group.

        Args:
            body (RequestBodyOne): body with group id

        Returns:
            models.Group: Entered group.

        Raises:
            ValidationEror: if group id is not provided
            NotFoundError: if group to enter does not exist
            ForbiddenError: if you try to enter closed group
            ForbiddenError: if group exceeds participants count
        """
        group_id = body.get('id')
        if group_id is None:
            raise exc.ValidationEror('Group id is a required property')

        group_to_enter = self.get(body)
        if group_to_enter is None:
            raise exc.NotFoundError('Requested group is not found')

        is_open = group_to_enter.get('is_open')
        if not is_open:
            raise exc.ForbiddenError(
                'This group is closed and requires admin approve')

        max_participants_count = group_to_enter.get('max_participants_count')

        all_participants = self.db.query(m.Participant).filter(
            getattr(m.Participant, 'group_id') == group_id).all()

        if len(all_participants) == max_participants_count:
            raise exc.ForbiddenError(
                'Group exceeds it\'s participants capabilities')

        new_participant = m.Participant(
            user_id=self.user.get('id'),
            group_id=group_id,
        )
        self._save_to_db(new_participant)
        return group_to_enter

    def leave_group(self, body: RequestBodyOne) -> dict:
        """Leave someones group.

        Args:
            body (RequestBodyOne): body with group id

        Returns:
            {} Empty response

        Raises:
            ValidationEror: if group id is not provided
            NotFoundError: if requested group does not exists
            NotFoundError: if you try to leave group that you are not part of
        """
        group_id = body.get('id')
        if group_id is None:
            raise exc.ValidationEror('Group id is a required property')

        group_to_leave = self.get(body)
        if group_to_leave is None:
            raise exc.NotFoundError('Requested group is not found')

        participant = (self.db.query(m.Participant)
                       .filter(and_(getattr(m.Participant, 'group_id') == group_id,
                                    getattr(m.Participant, 'user_id') == self.user.get('id')))
                       )

        if participant is None:
            raise exc.NotFoundError('You are not participant of this group')

        participant.delete(synchronize_session=False)
        self.db.commit()
        return {}
