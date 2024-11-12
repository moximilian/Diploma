"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
import app.models as m
from app.schemas import ItemCreate


class ItemsCRUD():
    def __innit__(self, db: Session):
        self.db = db
        pass
    def create_item(self, item: ItemCreate):
        db_item = m.Item(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def read_items(self, request_body):
        filters = request_body.get('filters')
        limit = filters.get('limit', 10)
        page = filters.get('limit', 1)
        return self.db.query(m.Item).offset(page).limit(limit).all()