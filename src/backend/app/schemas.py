from pydantic import BaseModel
from uuid import UUID


class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: UUID

    class Config:
        from_attributes = True