"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
from crud.events import EventsCRUD
import models as m
from crud.base import BaseCRUD
import api.exceptions as exc


class EventParticipansCRUD(BaseCRUD):
    
    def __init__(self, db: Session, auth_user):
        """ Initialize class.

        Args:
            db (Session): DB session
            auth_user (models.User): User that performs actions in this crud
        """
        super().__init__(db, m.EventParticipant)
        self.rapid = BaseCRUD(db, m.Rapid)
        self.event_ds = EventsCRUD(db, auth_user)
        self.user = auth_user
        
        
    def add_one_participant(self, body):
        event_id, user_id = body.get('id'), body.get('user_id')
        if event_id is None or user_id is None: raise exc.ValidationError()
        
        event = self.event_ds.get_item({'id': event_id})
        
        participant = self.db.query(m.Participant).filter_by(user_id = user_id, group_id = event.group_id).first()
        
        if participant is None: raise exc.NotFoundError()
        
        return self.insert({'event_id': event.id, 'participant_id': participant.id})
    
    def _make_output(self, rows):
        rows_new = []
        for row in rows:
            if row is None:
                continue
            row_dict = row.dict()
            row_dict['user_id'] = self.db.query(m.Participant).filter_by(id = row.participant_id).first().user_id
            rows_new.append(row_dict)
            
        return rows_new

         
    def add_all_group_participants(self, body):
        event_id  = body.get('id')
        if event_id is None: raise exc.ValidationError()
        
        event = self.event_ds.get_item({'id': event_id})
        
        participants = self.db.query(m.Participant).filter_by(group_id = event.group_id).all()
        if participants is None or len(participants) == 0: raise exc.NotFoundError()

        for participant in participants:
            event_participant = self.get_item(
                {'event_id': event.id, 'participant_id': participant.id},
                ['event_id', 'participant_id']
            )
            if event_participant is None:
                self.insert({'event_id': event.id, 'participant_id': participant.id})
        
        return {}