"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models as m
from crud.base import BaseCRUD
from schemas import EventInsertIn, RequestBodyOne
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
        super().__init__(db, m.Event, [m.Event, m.Rapid])
        self.rapid = BaseCRUD(db, m.Rapid)
        self.rapid_keys = ['weekdays', 'months', 'start_date', 'start_time', 'end_time']

        self.user = auth_user        

    def create_event(self, request_body: EventInsertIn):
        group_id, name = request_body.get('group_id'), request_body.get('name')
        if group_id is None or name is None:
            raise exc.ValidationEror('Group or name is not specified')
        
        found_item = self.db.query(m.Event).filter_by(name = name, group_id = group_id ).first()
        if found_item is not None:
            raise exc.ValidationEror('Such event already exists')
        
        rapid_request_body = {}
        item_request_body = {}
        for key, value in request_body.model_dump().items():
            if value is not None and value != '' and key in self.rapid_keys:
                rapid_request_body[key] = value
            else: item_request_body[key] = value
        if len(rapid_request_body.keys()) > 0:
            new_rapid = self.rapid.insert(rapid_request_body)[0]
            item_request_body['repeat_id'] = new_rapid.id
        
        return self.insert(item_request_body)
    
    def get(self, request_body: RequestBodyOne): 
        event = super().get_item(request_body)
        if (event.repeat_id is None): return event
        rapid = self.rapid.get_item({'id': event.repeat_id})
        rapid_dict = rapid.dict()
        return {**event.dict(), **rapid_dict}
    
    def _make_custom_query(self, query, wheres):
        new_wheres = []
        for where in wheres:
            if where['column'] == 'role':
                if where['value'] == 'teacher':
                    query = query = query.join(m.Rapid, m.Event.repeat_id == m.Rapid.id)\
                            .join(m.Group, m.Event.group_id == m.Group.id)\
                            .filter(m.Group.creator_id == self.user.get('id'))
                elif where['value'] == 'student':
                    query = query.join(m.Rapid, m.Event.repeat_id == m.Rapid.id)\
                        .join(m.Participant, m.Event.group_id == m.Participant.group_id)\
                        .filter(m.Participant.user_id == self.user.get('id'))
            else: new_wheres.append(where)

        return query, new_wheres

    def list(self, request_body: RequestBodyOne): 
        events = super().get_items(request_body)
        rows = []

        for event in events:
            if event.repeat_id is None: 
                rows.append(event)
                continue
            rapid = self.rapid.get_item({'id': event.repeat_id}).dict()
            rapid.pop('id')
            event_dict = event.dict()
            event_dict.pop('repeat_id')
            rows.append({**event_dict, **rapid})

        return super()._transform_response(rows)

    def update(self, request_body: EventInsertIn):
        group_id, name = request_body.get('group_id'), request_body.get('name')
        if group_id is None or name is None:
            raise exc.ValidationEror('Group or name is not specified')
        
        
        rapid_request_body = {}
        item_request_body = {}
        for key, value in request_body.model_dump().items():
            if value is not None and value != '' and key in [*self.rapid_keys, 'repeat_id']:
                if (key == 'repeat_id'): rapid_request_body['id'] = value
                else: 
                    rapid_request_body[key] = value
            else: 
                item_request_body[key] = value
        if len(rapid_request_body.keys()) > 0:
            new_rapid = self.rapid.update(rapid_request_body)[0]
            item_request_body['repeat_id'] = new_rapid.id
        
        return self.update(item_request_body)
