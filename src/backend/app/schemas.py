from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List, Any, Dict
import datetime

PASSWORD_PATTERN = r'^[a-zA-Z0-9!@#$%^&*()\-+=?]*$'


def PasswordField():
    return Field(min_length=8, max_length=128, pattern=PASSWORD_PATTERN)


def LoginField():
    return Field(min_length=1, max_length=128)


class BaseModelConfig(BaseModel):

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        return iter(self.model_dump().items())

    class Config:
        from_attributes = True


class ItemBase(BaseModelConfig):
    name: str
    description: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: UUID


class BaseItemIn(BaseModelConfig):
    id: UUID


# User

class UserBase(BaseModelConfig):
    name:  Optional[str] = None
    surname:  Optional[str] = None
    last_name:  Optional[str] = Field(min_length=0, max_length=189, default='')
    image_name:  Optional[str] = Field(
        min_length=0, max_length=256, default='')
    image_data:  Optional[bytes] = Field(default=b'', alias="image_data")


class UserCreate(UserBase):
    login: str = LoginField()
    password: str = PasswordField()
    password_confirm: str = PasswordField()


class UserOut(UserBase):
    id: UUID
    login: str = LoginField()
    password_set: bool = Field(default=True)
    registered_at: datetime.datetime


class UserInUpdate(UserBase):
    id: UUID

# Auth


class UserLogin(BaseModelConfig):
    login: str = LoginField()
    password: str = PasswordField()


class PasswordsChange(BaseModelConfig):
    current_password: str = PasswordField()
    new_password: str = PasswordField()
    new_password_confirm: str = PasswordField()

# Base Requests


class RequestBodyOne(BaseModelConfig):
    id: UUID


class RequestBodyList(BaseModelConfig):
    filters: dict = Field(default={})


class BaseListResponse(BaseModelConfig):
    rows: List[Any] = Field(default_factory=list)
    totalCount: int = Field(default=0)

# Token


class Token(BaseModelConfig):
    user_id: UUID
    access_token: str
    token_type: str = Field(default='bearer')

# Group


class GroupBase(BaseModelConfig):
    creator_id: UUID = None
    name: str
    description: str
    is_open: bool = Field(default=True)
    max_participants_count: int = Field(default=1)
    is_deleted: bool = Field(default=False)


class GroupOut(GroupBase):
    id: UUID


class GroupUpdateIn(BaseModelConfig):
    id: UUID
    name: str = None
    description: str = None
    is_open: bool = Field(default=True)
    max_participants_count: int = Field(default=1)


# Enter request


class BaseEnterRequestCreate(BaseModelConfig):
    group_id: UUID


class EnterRequestOut(BaseEnterRequestCreate):
    id: UUID
    user_id: UUID
    is_approved: Optional[bool] = None
    datetime: datetime.datetime


class EnterRequestUpdate(RequestBodyOne):
    is_approved: bool

# Event
# Insert in, Update in, Model


class EventModel(BaseModelConfig):
    id: UUID
    group_id: UUID
    repeat_id: UUID
    name: str = None
    description: str = None
    max_participants_count: int = Field(default=1)


class EventInsertIn(BaseModelConfig):
    group_id: UUID
    repeat_id: UUID
    name: str = None
    description: str = None
    max_participants_count: int = Field(default=1)


class EventUpdateIn(EventModel):
    pass

# Event participant


class EventParticipantModel(BaseModelConfig):
    id: UUID
    event_id: UUID
    datetime: datetime.datetime
    participant_id: UUID
    is_attended: bool
    is_paid: bool
    custom: Optional[Dict[str, Any]] = None


class EventParticipantInsertIn(BaseModelConfig):
    event_id: UUID
    datetime: datetime.datetime
    participant_id: UUID
    is_attended: bool
    is_paid: bool
    custom: Optional[Dict[str, Any]] = None


class EventParticipanUpdateIn(EventParticipantModel):
    pass

# Rapid


class RapidModel(BaseModelConfig):
    id: UUID
    weekdays: Optional[List[str, Any]] = None
    months: Optional[List[str, Any]] = None
    start_date: datetime.datetime
    end_date: datetime.datetime
    duration_mins: int = 1


class RapidInsertIn(BaseModelConfig):
    weekdays: Optional[List[str, Any]] = None
    months: Optional[List[str, Any]] = None
    start_date: datetime.datetime
    end_date: datetime.datetime
    duration_mins: int = 1


class RapidUpdateIn(RapidModel):
    pass

# Slot


class SlotModel(BaseModelConfig):
    id: UUID
    creator_id: UUID
    repeat_id: UUID
    name: str = None
    description: str = None
    max_participants_count: int = Field(default=1)
    datetime: datetime.datetime


class SlotInsertIn(BaseModelConfig):
    creator_id: UUID
    repeat_id: UUID
    name: str = None
    description: str = None
    max_participants_count: int = Field(default=1)
    datetime: datetime.datetime


class SlotUpdateIn(SlotModel):
    pass

# Slot Participant


class SlotParticipantModel(BaseModelConfig):
    id: UUID
    user_id: UUID
    slot_id: UUID
    is_attended: bool
    is_paid: bool
    custom: Optional[Dict[List, any]] = None
