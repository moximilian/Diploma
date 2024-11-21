from pydantic import BaseModel, Field
from uuid import UUID
import datetime

PASSWORD_PATTERN = r'^[a-zA-Z0-9!@#$%^&*()-+=?]*$'


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


class UserBase(BaseModelConfig):
    name: str
    surname: str
    last_name: str = Field(min_length=0, max_length=189, default='')
    login: str = LoginField()
    image_name: str = Field(min_length=0, max_length=256, default='')
    image_data: bytes = Field(default=b'', alias="image_data")


class UserCreate(UserBase):
    password: str = PasswordField()
    password_confirm: str = PasswordField()


class UserLogin(BaseModelConfig):
    login: str = LoginField()
    password: str = PasswordField()


class UserOut(UserBase):
    id: UUID
    password_set: bool = Field(default=True)
    registered_at: datetime.datetime


class Token(BaseModelConfig):
    access_token: str
    token_type: str = Field(default='bearer')

