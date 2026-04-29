from sqlalchemy.orm import Session
import models as m
import schemas
from crud.base import BaseCRUD
from crud.users import User

import base64


class Image(BaseCRUD):
    def __init__(self, db: Session, current_user: m.User):
        super().__init__(db, m.Image)
        self.current_user = current_user
        self.UserCRUD = User(db, current_user)

    def update_profile_pic(self, body: schemas.ImageCreate) -> m.Image:
        created_image = super().insert(body)[0]
        self.UserCRUD.update(
            {'id': self.current_user.id, 'photo_id': created_image.id})

        image_dict = created_image.dict()
        image_dict['image_data'] = self._to_base64(created_image.image_data)
        return image_dict

    def delete_profile_pic(self, body: schemas.ImageInOut):
        super().delete(body)
        self.UserCRUD.update({'id': self.current_user.id, 'photo_id': None})

    def _to_base64(self, value) -> str:
        return base64.b64encode(value)

    def get_image(self, body: schemas.RequestBodyOne) -> m.Image:
        image = super().get(body)

        image_dict = image.dict()
        image_dict['image_data'] = self._to_base64(image.image_data)
        return image_dict
