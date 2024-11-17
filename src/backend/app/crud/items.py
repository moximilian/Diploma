"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
import models as m
from schemas import ItemCreate


class ItemsCRUD():
    def __init__(self, db: Session):
        self.db = db

    def create_item(self, item: ItemCreate):
        db_item = m.Item(name = item.name, description = item.description)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def read_items(self, request_body):
        filters = request_body.get('filters')
        limit = filters.get('limit', 10)
        page = filters.get('page', 1)
        return self.db.query(m.Item).offset(page).limit(limit).all()