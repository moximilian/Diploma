"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import models as m
from crud.base import BaseCRUD
from schemas import GroupOut, RequestBodyOne, GroupBase
import api.exceptions as exc


class GroupsCRUD(BaseCRUD):
    """CRUD logic to work with groups.
    """

    def __init__(self, db: Session, auth_user):
        """ Initialize class.

        Args:
            db (Session): DB session
            auth_user (models.User): User that performs actions in this crud
        """
        super().__init__(db, m.Group)
        self.user = auth_user

    def create_group(self, request_body: GroupBase) -> m.Group:
        """ Create group based on given parametres.

        Args:
            item (GroupBase): Parametres for new group to create

        Returns:
            models.Group: new created group with ID
        """

        request_body.creator_id = self.user.get('id')
        new_group = super().insert(request_body)
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

        group_to_enter = self.get_item(body)
        if group_to_enter is None:
            raise exc.NotFoundError('Requested group is not found')

        is_open = group_to_enter.get('is_open')
        if not is_open:
            raise exc.ForbiddenError(
                'This group is closed and requires admin approve')

        max_participants_count = group_to_enter.get('max_participants_count')

        all_participants = group_to_enter.participants

        if len(all_participants) == max_participants_count:
            raise exc.ForbiddenError(
                'Group exceeds it\'s participants capabilities')

        new_participant = m.Participant(
            user_id=self.user.get('id'),
            group_id=group_id,
        )
        self._save_to_db(new_participant)
        return group_to_enter

    def _make_custom_query(self, query, wheres):
        new_wheres = []
        for where in wheres:
            if where.get('column') == 'is_currrent_participant':
                where = super()._transform_boolean(where)
                is_paricipant = where.get('value')
                if is_paricipant:
                    query = query.join(m.Participant, getattr(m.Group, 'id') == getattr(
                        m.Participant, 'group_id')).where(getattr(m.Participant, 'user_id') == self.user.id)
                else:
                    query = query.outerjoin(m.Participant, getattr(m.Group, 'id') == getattr(
                        m.Participant, 'group_id')).where(or_(
                            m.Participant.user_id.is_(None),  # Нет участников
                            m.Participant.user_id != self.user.id
                        ))
                continue
            if where.get('column') == 'participant_id':
                participant_id = where.get('value')
                query = query.join(m.Participant, getattr(m.Group, 'id') == getattr(
                    m.Participant, 'group_id')).where(getattr(m.Participant, 'user_id') == participant_id)
                continue
            new_wheres.append(where)
        return query, new_wheres

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

        group_to_leave = self.get_item(body)
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

    def _make_output(self, rows):
        result = []
        for row in rows:
            if row is None:
                continue
            row_dict = row.dict()
            is_participant = [
                participant for participant in row.participants if participant.user_id == self.user.id]
            row_dict['is_participant'] = len(is_participant) != 0
            row_dict['participant_count'] = len(row.participants)
            result.append(row_dict)

        return result

    def list(self, request_body):
        filters = request_body.get('filters')
        wheres = filters.get('wheres')

        new_wheres = []
        for where in wheres:
            if where['column'] == 'creator_id' and (where['value'] == 'false' or where['value'] == 'null'):
                where['condition'] = '!='
                where['value'] = self.user.id
            new_wheres.append(where)
        return super().list({
            'filters': {
                'wheres': new_wheres,
                'orders': filters.get('orders', [])
            }
        })
