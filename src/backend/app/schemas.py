from pydantic import BaseModel, Field, field_validator, field_serializer
from uuid import UUID
from typing import Optional, List, Any, Dict, Union
import datetime
import base64
from api import exceptions as exc

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
    photo_id: Optional[UUID] = None

    role_name: str = Field(min_length=1, default='student')
    is_external_auth: bool = Field(default=False)


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

# Image

class ImageCreate(BaseModelConfig):
    image_name: str = Field(),
    image_data: Union[bytes, str]

     # Валидатор для преобразования base64 строки в bytes
    @field_validator('image_data', mode='before')
    def decode_base64(cls, value):
        if isinstance(value, str):
            # Убираем префикс "data:image/png;base64," если он есть
            if value.startswith('data:'):
                value = value.split(',', 1)[1]
            try:
                return base64.b64decode(value)
            except Exception:
                raise exc.InternalError()
        return value

class ImageInOut(ImageCreate):
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
class RequestBodyOnes(BaseModelConfig):
    ids: List[UUID]

class RequestBodyOne(BaseModelConfig):
    id: UUID


class RequestBodyList(BaseModelConfig):
    filters: dict = Field(default={})

# Base Responses

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
    is_participant: bool = Field(default=True)


class GroupUpdateIn(BaseModelConfig):
    id: UUID
    name: str = None
    description: str = None
    is_open: bool = Field(default=True)
    max_participants_count: int = Field(default=1)

class ParticipantCreate(BaseModelConfig):
    user_id: UUID
    group_id: UUID


class Participant(BaseModelConfig):
    id: UUID
    user_id: UUID
    group_id: UUID

# Enter request


class BaseEnterRequestCreate(BaseModelConfig):
    group_id: UUID


class EnterRequestOut(BaseEnterRequestCreate):
    id: UUID
    user_id: UUID
    is_approved: Optional[bool] = None
    datetime: datetime.datetime



# Event
# Insert in, Update in, Model

class EventModelOut(BaseModelConfig):
    id: UUID
    repeat_id: UUID
    group_id: UUID

    weekdays: list = None
    months: list = None
    start_date: datetime.date = None
    start_time: datetime.time = None
    end_time: datetime.time = None

    name: str = None
    description: Optional[str] = None
    price: int = None
    
    @field_serializer('description')
    def serialize_description(self, description: Optional[str]) -> Optional[str]:
        return '' if description is None else description

    @field_serializer('start_date')
    def serialize_date(self, dt: Optional[datetime.date]) -> Optional[str]:
        return dt.strftime('%d-%m-%Y') if dt else None
class EventModel(BaseModelConfig):
    id: UUID
    repeat_id: UUID
    group_id: UUID

    weekdays: list = None
    months: list = None
    start_date: datetime.date = None
    start_time: datetime.time = None
    end_time: datetime.time = None

    name: str = None
    description: str = None
    price: int =None
    
    @field_validator('start_date', mode='before')
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                # Парсинг формата dd.mm.yyyy
                day, month, year = map(int, value.split('.'))
                return datetime.date(year, month, day)
            except ValueError:
                try:
                    # Парсинг формата dd-mm-yyyy
                    day, month, year = map(int, value.split('-'))
                    return datetime.date(year, month, day)
                except ValueError:
                    raise exc.ValidationEror("Date must be in format dd.mm.yyyy or dd-mm-yyyy")
        return value


class EventInsertIn(BaseModelConfig):
    group_id: UUID

    weekdays: list = None
    months: list = None
    start_date: datetime.date = None
    start_time: datetime.time = None
    end_time: datetime.time = None

    name: str = None
    description: str = None
    price: int =None

    @field_validator('start_date', mode='before')
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                # Парсинг формата dd.mm.yyyy
                day, month, year = map(int, value.split('.'))
                return datetime.date(year, month, day)
            except ValueError:
                try:
                    # Парсинг формата dd-mm-yyyy
                    day, month, year = map(int, value.split('-'))
                    return datetime.date(year, month, day)
                except ValueError:
                    raise exc.ValidationEror("Date must be in format dd.mm.yyyy or dd-mm-yyyy")
        return value


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
    weekdays: List[Any] = None
    months: List[Any] = None
    start_date: datetime.datetime
    end_date: datetime.datetime
    duration_mins: int = 1


class RapidInsertIn(BaseModelConfig):
    weekdays: List[Any] = None
    months: List[Any] = None
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
    custom: Dict[List[Any], Any] = None
