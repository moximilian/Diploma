"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_

import models as m
from crud.base import BaseCRUD
from crud.groups import GroupsCRUD
from schemas import GroupOut, RequestBodyOne
import api.exceptions as exc

class EnterRequestsCRUD(BaseCRUD):

    def __init__(self, db, user):
        self.user = user
        super().__init__(db, m.EnterRequest)

    def create_enter_request(self, body):
        group_id = body.get('group_id')
        if group_id is None:
            raise exc.NotFoundError('Group id is not provided')
        
        group = self.get({'id': group_id}, 'id', m.Group)
        if group is None:
            raise exc.NotFoundError('Group is not found')
        
        is_group_open = group.get('is_open', False)
        if is_group_open:
            return GroupsCRUD(self.db, self.user).enter_group({'id': group_id})

        new_enter_request = m.EnterRequest(
            user_id = self.user.get('id'),
            group_id = group_id
        )
        new_enter_request = self._save_to_db(new_enter_request)
        return new_enter_request

    def _check_request_valid(self, body):
        request = self.get(body)
        group_id = request.get('group_id')

        group = self.get({'id': group_id}, 'id', m.Group)
        creator_id = group.get('creator_id')
        return creator_id == self.user.get('id')

    def approve_request(self, body):
        if not self._check_request_valid(body):
            raise exc.ForbiddenError('You cant modify this request')

        request_body = {
            'id': body.get('id'),
            'is_approved': True
        }
        return self.update(request_body)

    def revoke_request(self, body):
        if not self._check_request_valid(body):
            raise exc.ForbiddenError('You cant modify this request')

        request_body = {
            'id': body.get('id'),
            'is_approved': False
        }
        return self.update(request_body)
    
    def delete_request(self, body):
        request_id = body.get('id')
        request = self.get(body)

        if request.get('user_id') != self.user.get('id'):
            raise exc.ForbiddenError('You can not delete this request')
        
        return self.delete(body)

    def _get_incoming_requests(self, query):
        query = (query
            .join(m.Group, m.EnterRequest.group_id == m.Group.id)
            .filter(m.Group.creator_id == self.user.get('id'), m.Group.is_open == False, m.Group.is_deleted == False)
        )
        return query

    def _get_outgoing_requests(self, query):
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
                    raise exc.ValidationEror('Specified type is not valid: only OUTGOING or INCOMING', field= 'type')
                query = type_function.get(value)(query)
            else:
                query = query.filter(getattr(m.EnterRequest, column) == where.get('value'))

        rows = query.all()

        return self._transform_response(rows, len(rows))
