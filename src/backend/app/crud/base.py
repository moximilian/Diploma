import models as m
import api.exceptions as exc


class BaseCRUD():
    """BaseCRUD implements base common logic that can be used
    by all other CRUD classes.

    Args:
        db: SqlAlchemy Session instance
    """

    def __init__(self, db, model):
        self.db = db
        self.model = model

    def _save_to_db(self, item):
        """Create new Item in db and return its new glory.

        Args:
            item: children of BaseModel

        Returns:
            created_item: children of BaseModel
        """
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get(self, body, field='id'):
        """Get one item from specific table by given field key and value.

        Args:
            value (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.\n
            None if provided field is not found on model.
        """
        if not hasattr(self.model, field):
            raise exc.NotFoundError(field=field)

        value = body.get(field)
        return self.db.query(self.model).filter(getattr(self.model, field) == value).first()

    def delete(self, body, field='id'):
        """Delete one item from specific table by given field key and value.

        Args:
            body (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.\n
            None if provided field is not found on model.
        """
        if not hasattr(self.model, field):
            raise exc.NotFoundError(field=field)

        item_to_delete = self.get(body)
        if not item_to_delete:
            raise exc.NotFoundError(field=field)
        self.db.delete(item_to_delete)
        self.db.commit()
        self.db.refresh(item_to_delete)
        return item_to_delete
    
    def _is_value_empty(self, value) -> bool:
        null_values = [None, '', 'null', 'None', b'']
        return value in null_values

    def _is_immutable_field(self, field) -> bool:
        immutable_fields = ['id', 'login']
        return field in immutable_fields
    
    def update(self, body):
        """Update one item from one specific table by given fields

        Args:
            body (schemas.RequestBodyOne) Request body

        Returns:
            Item in DB that was found in db.\n
        """
        item_to_update = self.get(body)
        if not item_to_update:
            raise exc.NotFoundError()
        for key, value in body.dict().items():
            if not self._is_value_empty(value) and not self._is_immutable_field(key):
                # print(f'Updated field {key} with value = {value}')
                setattr(item_to_update, key, value)
        
        self.db.commit()
        self.db.refresh(item_to_update)
        
        return item_to_update

    def mark_deleted(self, body, field):
        """Mark one item as deleted from specific table by given field key and value.

        Args:
            value (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.\n
            None if provided field is not found on model.
        """
        if not hasattr(self.model, field):
            raise exc.NotFoundError(field=field)
        if not hasattr(self.model, 'is_deleted'):
            print(f'{self.model} do not have `is_deleted` property')
            raise exc.InternalError()

        item_to_delete = self.get(body)
        if not item_to_delete:
            raise exc.NotFoundError(field=field)

        value_to_search = body.get(field, None)
        if not value_to_search:
            raise exc.NotFoundError(field=field)
        self.db.update(self.model).where(
            self.model[field] == value_to_search).values(is_deleted=True)
        self.db.commit()
