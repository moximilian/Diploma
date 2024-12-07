from sqlalchemy.orm import Session
import models as m
import typing as t
import api.exceptions as exc
import schemas
from crud.base import BaseCRUD
import bcrypt
from crud.auth import Authorisation


class User(BaseCRUD):
    def __init__(self, db: Session, current_user: m.User):
        super().__init__(db, m.User)
        self.current_user = current_user
        self.authCRUD = Authorisation(db)

    def change_password(self, body: schemas.PasswordsChange) -> m.User:
        current_password = body.current_password
        if not self.authCRUD._verify_password(current_password, self.current_user.password):
            raise exc.ValidationEror('Current password is not valid', field='current_password')
        if (body.get('new_password') != body.get('new_password_confirm')):
            raise exc.ValidationEror('Passwords do not match', field=['new_password', 'new_password_confirm'])

        hashed_new_password = self.authCRUD._hash_password(body.get('new_password'))

        self.current_user = self.db.update(m.User).where(m.User.id == self.current_user.id ).values(password=hashed_new_password)
        self.db.commit()
        self.db.refresh(self.current_user)
        return self.current_user

