"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_

import models as m
from crud.base import BaseCRUD
from crud.groups import GroupsCRUD
from crud.participants import ParticipantsCRUD

from crud.users import User

from schemas import GroupOut, RequestBodyOne, BaseEnterRequestCreate, RequestBodyOne, EnterRequestOut, ParticipantCreate
import api.exceptions as exc


class EnterRequestsCRUD(BaseCRUD):

    def __init__(self, db, user):
        self.user = user
        self.userCRUD = User(db, user)
        self.groupCRUD = GroupsCRUD(db, user)
        self.participant = ParticipantsCRUD(db, user)
        super().__init__(db, m.EnterRequest)

    def create_enter_request(self, body: BaseEnterRequestCreate) -> m.EnterRequest:
        """Create request to enter closed group.

        Args:
            body (BaseEnterRequestCreate): Body with 'group_id' in it

        Returns:
            models.EnterRequest: Newly created enrty request

        Raises:
            ValidationEror: if group_id is not proveded
            NotFoundError: if group is not exists
        """
        group_id = body.get('group_id')
        if group_id is None:
            raise exc.ValidationEror('Group id is not provided')

        group = self.get({'id': group_id}, 'id', m.Group)
        if group is None:
            raise exc.NotFoundError('Group is not found')

        is_group_open = group.get('is_open', False)
        if is_group_open:
            return self.groupCRUD.enter_group({'id': group_id})

        new_enter_request = m.EnterRequest(
            user_id=self.user.get('id'),
            group_id=group_id
        )
        new_enter_request = self._save_to_db(new_enter_request)
        return new_enter_request

    def _check_request_valid(self, body: RequestBodyOne) -> bool:
        """Check if enter request for group that you created.

        Args:
            body (RequestBodyOne): request with request id

        Returns:
            boolean
        """
        request = self.get(body)
        group_id = request.get('group_id')

        group = self.get({'id': group_id}, 'id', m.Group)
        creator_id = group.get('creator_id')
        return creator_id == self.user.get('id')

    def approve_request(self, body: RequestBodyOne):
        """Approve request to your group and let user enter group.

        Args:
            body (RequestBodyOne): request with request id

        Returns:
            models.EnterRequest: approved enter request

        Raises:
            ForbiddenError: if you try to approve request group without being it creator
        """
        if not self._check_request_valid(body):
            raise exc.ForbiddenError('You cant modify this request')

        request_approve_body = {
            'id': body.get('id'),
            'is_approved': True
        }

        approved_request = self.update(request_approve_body)

        is_not_participant = self.participant.get({'user_id': approved_request.get('user_id')}, 'user_id')
        if (is_not_participant is None):
            self.participant.insert(ParticipantCreate(
                user_id=approved_request.get('user_id'),
                group_id= approved_request.get('group_id')
            ), m.Participant)
        return approved_request

    def revoke_request(self, body: EnterRequestOut):
        """Revoke request to your group.

        Args:
            body (RequestBodyOne): request with request id

        Returns:
            models.EnterRequest: revoked enter request

        Raises:
            ForbiddenError: if you try to revoke request group without being it creator
        """
        if not self._check_request_valid(body):
            raise exc.ForbiddenError('You cant modify this request')

        request_body = {
            'id': body.get('id'),
            'is_approved': False
        }
        return self.update(request_body)

    def delete_request(self, body: EnterRequestOut):
        """Delete your enter request.

        Args:
            body (EnterRequestOut): body with request id

        Returns:
            models.EnterRequest: deleted enter request

        Raises:
            ForbiddenError: if you try to delete someone else request

        """
        request_id = body.get('id')
        request = self.get(body)

        if request.get('user_id') != self.user.get('id'):
            raise exc.ForbiddenError('You can not delete this request')

        return self.delete(body)

    def _get_incoming_requests(self, query):
        """Get query of incomming enter requests to all your closed groups.

        Args:
            query: Base query

        Returns:
            query
        """
        query = (query
                 .join(m.Group, m.EnterRequest.group_id == m.Group.id)
                 .filter(
                     m.Group.creator_id == self.user.get('id'),
                     m.Group.is_open == False,
                     m.Group.is_deleted == False
                 ))
        return query

    def _get_outgoing_requests(self, query):
        """Get query of outgoing enter requests to all your groups you want enter.

        Args:
            query: Base query

        Returns:
            query
        """
        query = query.filter(m.EnterRequest.user_id == self.user.get('id'))
        return query

    def read_items(self, body):
        """Read request items with request body for list request.
            Provide 'type' filter param to specify:
                INCOMING: requests by other users to groups you created
                OUTGOING: your sent request
            group_ids - optional param to specify groups of which to show requests

        Args:
            body (dict): request body with filters

        Returns:
            BaseListResponse

        Raises:
            ValidationEror: if you tried to get unknown type of requests
        """
        filters = body.get('filters', {})
        wheres = filters.get('wheres', [])

        type_function = {
            'INCOMING': self._get_incoming_requests,
            'OUTGOING': self._get_outgoing_requests
        }
        query = self.db.query(m.EnterRequest)
        for where in wheres:
            column = where.get('column')
            if column == 'type':
                value = where.get('value')
                if value not in type_function.keys():
                    raise exc.ValidationEror(
                        'Specified type is not valid: only OUTGOING or INCOMING', field='type')
                query = type_function.get(value)(query)
            else:
                query = query.filter(
                    getattr(m.EnterRequest, column) == where.get('value'))
        rows = query.all()

        return self._transform_response(rows, len(rows))
