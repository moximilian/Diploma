"""
DB Models
"""
import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    ForeignKey,
    Integer,
    Boolean,
    false,
    LargeBinary,
    JSON,
    PickleType,
    Time,
    Date
)
from sqlalchemy.ext.mutable import MutableList

from sqlalchemy.orm import class_mapper, ColumnProperty, relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def dict(self):
        result = {}
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                result[prop.key] = getattr(self, prop.key)
        return result


class Item(Base, BaseModel):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    description = Column(String)


class User(Base, BaseModel):
    __tablename__ = 'users'

    photo_id = Column(
        UUID(as_uuid=True),
        ForeignKey('images.id', onupdate='CASCADE', ondelete='SET NULL'), nullable=True
    )

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    name = Column(String(128), nullable=False)
    surname = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    login = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    registered_at = Column('registered_at',
                           DateTime(), default=func.now())
    failed_attempts_count = Column(Integer(), server_default='0')
    is_deleted = Column(Boolean, default=False, server_default=false())
    role_name=Column(String(128), nullable=False, server_default='sudent')
    is_external_auth = Column(Boolean, default=False, server_default=false())

    # Relationships
    photo = relationship("Image", backref="user", foreign_keys=[photo_id])
    created_groups = relationship(
        "Group", backref="creator", foreign_keys="Group.creator_id")
    created_slots = relationship(
        "Slot", backref="creator", foreign_keys="Slot.creator_id")
    enter_requests = relationship(
        "EnterRequest", backref="user", foreign_keys="EnterRequest.user_id")
    participants = relationship(
        "Participant", backref="user", foreign_keys="Participant.user_id")
    slot_participants = relationship(
        "SlotParticipant", backref="user", foreign_keys="SlotParticipant.user_id")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._groups = []

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, group):
        self._groups.append(group)


class RevokedToken(Base, BaseModel):
    __tablename__ = 'revoked_tokens'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    token = Column(String, unique=True)
    revoked_at = Column(DateTime, default=func.now())


class Image(Base, BaseModel):
    __tablename__ = 'images'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    image_name = Column(String(256), nullable=False)
    image_data = Column(LargeBinary(length=(2**32)-1), default=b'')


class Group(Base, BaseModel):
    __tablename__ = 'groups'
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False
    )
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=True)
    is_open = Column(Boolean, default=False, nullable=False)
    max_participants_count = Column(Integer)
    is_deleted = Column(Boolean, default=False, server_default=false())

    # Relationships
    enter_requests = relationship(
        "EnterRequest", backref="group", foreign_keys="EnterRequest.group_id")
    participants = relationship(
        "Participant", backref="group", foreign_keys="Participant.group_id")
    events = relationship("Event", backref="group",
                          foreign_keys="Event.group_id")


class EnterRequest(Base, BaseModel):
    __tablename__ = 'group_enter_requests'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    datetime = Column('datetime',
                      DateTime(), default=func.now())
    is_approved = Column(Boolean, default=None, nullable=True)


class Participant(Base, BaseModel):
    __tablename__ = 'group_participants'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )

    events = relationship("EventParticipant", backref="participant",
                          foreign_keys="EventParticipant.participant_id")


class Event(Base, BaseModel):
    __tablename__ = 'events'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=True)


    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )

    repeat_id = Column(
        UUID(as_uuid=True),
        ForeignKey('rapids.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=True
    )

    price = Column(Integer, nullable = True)

    event_participants = relationship(
        "EventParticipant", backref="event", foreign_keys="EventParticipant.event_id")


class EventParticipant(Base, BaseModel):
    __tablename__ = 'event_participants'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)

    event_id = Column(
        UUID(as_uuid=True),
        ForeignKey('events.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False
    )
    datetime = Column('datetime',
                      DateTime(), default=func.now())
    participant_id = Column(
        UUID(as_uuid=True),
        ForeignKey('group_participants.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False
    )

    is_attended = Column(Boolean, default=None, nullable=True)
    is_paid = Column(Boolean, default=None, nullable=True)

    custom = Column(JSON, default=None, nullable=True)


class Rapid(Base, BaseModel):
    __tablename__ = 'rapids'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)

    weekdays = Column(MutableList.as_mutable(PickleType),
                      default=[])

    months = Column(MutableList.as_mutable(PickleType),
                    default=[])

    start_date = Column('start_date',
                        Date(), default=func.now())
    start_time = Column('start_time',
                      Time(), nullable=True)

    end_time = Column('end_time',
                    Time(), nullable=True)
    

    events = relationship("Event", backref="rapid",
                          foreign_keys="Event.repeat_id")
    slots = relationship("Slot", backref="rapid",
                         foreign_keys="Slot.repeat_id")


class Slot(Base, BaseModel):
    __tablename__ = 'slots'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)

    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False
    )
    repeat_id = Column(
        UUID(as_uuid=True),
        ForeignKey('rapids.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False
    )
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=True)
    max_participants_count = Column(Integer, server_default='1')
    datetime = Column('datetime',
                      DateTime(), default=func.now())

    participants = relationship(
        "SlotParticipant", backref="slot", foreign_keys="SlotParticipant.slot_id")


class SlotParticipant(Base, BaseModel):
    __tablename__ = 'slot_participants'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False
    )
    slot_id = Column(
        UUID(as_uuid=True),
        ForeignKey('slots.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False
    )
    is_attended = Column(Boolean, default=None, nullable=True)
    is_paid = Column(Boolean, default=None, nullable=True)

    custom = Column(JSON, default=None, nullable=True)
