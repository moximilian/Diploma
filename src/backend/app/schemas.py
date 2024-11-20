from pydantic import BaseModel, Field
from uuid import UUID
import datetime


class BaseModelConfig(BaseModel):

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


class UserBase(BaseModelConfig):
    name: str
    surname: str
    last_name: str = Field(min_length=1, max_length=189, default='')
    login: str = Field(min_length=1, max_length=128)
    image_name: str = Field(min_length=0, max_length=256, default='')
    image_data: bytes = Field(default=b'', alias="image_data")


class UserCreate(UserBase):
    # TODO move to external file with ENUMS
    password: str = Field(min_length=8, max_length=128,
                          pattern=r'^[a-zA-Z0-9!@#$%^&*()-+=?]*$')
    password_confirm: str = Field(
        min_length=8, max_length=128, pattern=r'^[a-zA-Z0-9!@#$%^&*()-+=?]*$')


class UserLogin(BaseModel):
    login: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=8, max_length=128)


class UserOut(UserBase):
    id: UUID
    password_set: bool = Field(default=True)
    registered_at: datetime.datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthSession(BaseModelConfig):
    sid: UUID
    expired: datetime.datetime
    status: str
    user_id: str
