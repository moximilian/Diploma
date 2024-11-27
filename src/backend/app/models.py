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
    LargeBinary
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)


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
        ForeignKey('images.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    name = Column(String(128), nullable=False)
    surname = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    login = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    registered_at = Column('password_expires_at',
                           DateTime(), default=func.now())
    failed_attempts_count = Column(Integer(), server_default='0')
    is_deleted = Column(Boolean, default=False, server_default=false())


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
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=True)
    is_open = Column(Boolean, default=False, server_default=false())
    max_participants_count = Column(Integer, server_default='1')
    is_deleted = Column(Boolean, default=False, server_default=false())


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
    is_approved = Column(Boolean, default=False, server_default=false())


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

class Event(Base, BaseModel):
    __tablename__ = 'events'

    id = Column(UUID(as_uuid=True), primary_key=True,
                    default=uuid.uuid4, index=True)

    userepeat_id = Column(
        UUID(as_uuid=True),
        ForeignKey('rapids .id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=True)
    datetime = Column('datetime',
                           DateTime(), default=func.now())
    duration = Column(Integer(), server_default='0')
    max_participants_count = Column(Integer, server_default='1')
