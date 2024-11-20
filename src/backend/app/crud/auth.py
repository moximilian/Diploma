
"""
Logic to work with DB
"""
from sqlalchemy.orm import Session
import models as m
from schemas import UserCreate, UserOut
from fastapi import HTTPException, status
from crud.base import BaseCRUD
import api.exceptions as exc
import bcrypt


class Authorisation(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db)

    def register(self, body: UserCreate):

        login = body.login
        existing_user = self.db.query(m.User).where(
            m.User.login == login).first()
        if (existing_user and existing_user.is_deleted == False):
            raise exc.ValidationEror(message='Username already registered', field='login')

        password = body.password
        password_confirm = body.password_confirm
        if (password != password_confirm):
            raise exc.ValidationEror(message='Passwords do not match', field='password_confirm')

        hashed_password = self._hash_password(password)

        added_image = self._add_image(body)

        new_user = m.User(name=body.name,
                          surname=body.surname,
                          last_name=body.last_name,
                          login=login,
                          password=hashed_password,
                          photo_id=added_image.id if added_image is not None else None
                          )
        new_user = self._save_to_db(new_user)
        return new_user

    def _add_image(self, body) -> str:
        image_name = body.image_name or ''

        if not image_name:
            return None

        new_image = m.Image(image_name=image_name,
                            image_data=body.image_data)
        return self._save_to_db(new_image)

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def login():
        pass

    def logout():
        pass

    # def create_item(self, item: ItemCreate):
    #     db_item = m.Item(name = item.name, description = item.description)
    #     self.db.add(db_item)
    #     self.db.commit()
    #     self.db.refresh(db_item)
    #     return db_item

    # def read_items(self, request_body):
    #     filters = request_body.get('filters')
    #     limit = filters.get('limit', 10)
    #     page = filters.get('page', 1)
    #     return self.db.query(m.Item).offset(page).limit(limit).all()
