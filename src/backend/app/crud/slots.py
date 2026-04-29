"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
import models as m
from crud.base import BaseCRUD
from schemas import SlotInsertIn, RequestBodyOne, SlotModel, RequestBodyList
import api.exceptions as exc


class SlotsCRUD(BaseCRUD):
    def __init__(self, db: Session, auth_user):
        """ Initialize class.

            Args:
                db (Session): DB session
                auth_user (models.User): User that performs actions in this crud
            """
        super().__init__(db, m.Slot, [m.Slot, m.Rapid])
        self.rapid = BaseCRUD(db, m.Rapid)
        self.participants_ds = BaseCRUD(db, m.SlotParticipant)
        self.rapid_keys = ['weekdays', 'months',
                           'start_date', 'start_time', 'end_time', 'repeat_id']

        self.user = auth_user

    def create_slot(self, request_body: SlotInsertIn):
        name = request_body.get('name')

        found_item = self.db.query(m.Slot).filter_by(name=name).first()
        if found_item is not None:
            raise exc.ValidationEror('Such slot already exists')

        rapid_request_body = {}
        item_request_body = {}
        for key, value in request_body.model_dump().items():
            if value is not None and value != '' and key in self.rapid_keys:
                rapid_request_body[key] = value
            else:
                item_request_body[key] = value
        if len(rapid_request_body.keys()) > 0:
            new_rapid = self.rapid.insert(rapid_request_body)[0]
            item_request_body['repeat_id'] = new_rapid.id

        return self.insert(item_request_body)

    def get(self, request_body: RequestBodyOne):

        slot = super().get_item(request_body)
        is_participant = [
            participant for participant in slot.participants if participant.user_id == self.user.id]
        participant_dict = {
            'is_participant': len(is_participant) != 0,
            'participants_count': len(slot.participants)
        }
        if (slot.repeat_id is None):
            return slot
        rapid = self.rapid.get_item({'id': slot.repeat_id})
        rapid_dict = rapid.dict()
        return {**slot.dict(), **rapid_dict, **participant_dict}

    def _make_custom_query(self, query, wheres):
        new_wheres = []
        for where in wheres:
            if where['column'] == 'role' and where['value'] == 'teacher':
                query = query = query.join(m.Rapid, m.Slot.repeat_id == m.Rapid.id)\
                    .filter(m.Slot.creator_id == self.user.get('id'))
            elif where['column'] == 'only_my' and where['value'] == True:
                query = query.join(m.Rapid, m.Slot.repeat_id == m.Rapid.id)\
                    .join(m.SlotParticipant, m.SlotParticipant.slot_id == m.Slot.id)\
                    .filter(m.SlotParticipant.user_id == self.user.get('id'))
            else:
                new_wheres.append(where)

        return query, new_wheres

    def list(self, request_body: RequestBodyList):
        slots = super().get_items(request_body)
        rows = []

        filters = request_body.get('filters', {})
        wheres = filters.get('wheres', [])

        is_filter_by_creator_id = len(
            [where for where in wheres if where['column'] == 'creator_id']) != 0
        is_filter_asked_by_teacher = len(
            [where for where in wheres if where['column'] == 'role' and where['value'] == 'teacher']) != 0

        if not is_filter_asked_by_teacher and not is_filter_by_creator_id:
            return super()._transform_response([])

        for slot in slots:
            if slot.repeat_id is None:
                rows.append(slot)
                continue
            rapid = self.rapid.get_item({'id': slot.repeat_id}).dict()
            rapid.pop('id')
            slot_dict = slot.dict()
            slot_dict.pop('repeat_id')
            slot_dict['participants_count'] = len(slot.participants)
            rows.append({**slot_dict, **rapid})

        return super()._transform_response(rows)

    def update(self, request_body: SlotModel):
        slot_id = request_body.get('id')
        if slot_id is None:
            raise exc.ValidationEror('ID is not specified')

        rapid_request_body = {}
        item_request_body = {}
        for key, value in request_body.model_dump().items():
            if value is not None and value != '' and key in self.rapid_keys:
                if (key == 'repeat_id'):
                    rapid_request_body['id'] = value
                else:
                    rapid_request_body[key] = value
            else:
                item_request_body[key] = value
        new_rapid_dict = {}
        if len(rapid_request_body.keys()) > 0:
            new_rapid = self.rapid.update(rapid_request_body)
            item_request_body['repeat_id'] = new_rapid.id
        updated_slot = super().update(item_request_body)

        new_rapid_dict = new_rapid.dict()
        new_rapid_dict.pop('id', None)
        return {**updated_slot.dict(), **new_rapid_dict}

    def enter(self, request_body: RequestBodyOne):
        slot_id = request_body.get('id')
        if slot_id is None:
            raise exc.ValidationEror()

        found_items = self.participants_ds.get_items({'filters': {
            'wheres': [{
                'column': 'user_id',
                'value': self.user.get('id')
            }, {
                'column': 'slot_id',
                'value': slot_id
            }]
        }})
        if found_items is not None and len(found_items) > 0:
            raise exc.ValidationEror('You already participate in this slot')

        slot = super().get_item({'id': slot_id})

        if len(slot.participants) == slot.max_participants_count:
            raise exc.ForbiddenError('Slot exceeds it\'s maximum capacity')

        self.participants_ds.insert({
            'user_id': self.user.get('id'),
            'slot_id': slot_id,
        })
        return {}

    def leave(self, request_body: RequestBodyOne):
        slot_id = request_body.get('id')
        if slot_id is None:
            raise exc.ValidationEror()

        found_items = self.participants_ds.get_items({'filters': {
            'wheres': [{
                'column': 'user_id',
                'value': self.user.get('id')
            }, {
                'column': 'slot_id',
                'value': slot_id
            }]
        }})

        if found_items is None or len(found_items) == 0:
            raise exc.ValidationEror('You do not participate in this slot')

        return self.participants_ds.delete({
            'id': found_items[0].id
        })
