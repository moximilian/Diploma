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


class Item(Base):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    description = Column(String)


class User(Base):
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


class AuthSession(Base):
    __tablename__ = 'auth_sessions'

    sid = Column(UUID(as_uuid=True), primary_key=True,
                 default=uuid.uuid4, index=True)
    expired = Column(DateTime(), nullable=True)
    status = Column(String(256), nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
    )


class Image(Base):
    __tablename__ = 'images'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    image_name = Column(String(256), nullable=False)
    image_data = Column(LargeBinary(length=(2**32)-1), default=b'')
