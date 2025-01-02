import models as m
import api.exceptions as exc
from schemas import BaseListResponse


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

    def get(self, body, field='id', model = None):
        """Get one item from specific table by given field key and value.

        Args:
            value (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.\n
            None if provided field is not found on model.
        """
        model = self.model if model is None else model

        if not hasattr(self.model, field):
            raise exc.NotFoundError(field=field)

        query = self.db.query(model)

        value = body.get(field)
        if value is None:
            raise exc.NotFoundError(field=field)
        found_item =  query.filter(getattr(model, field) == value).first()
        if not found_item or found_item.get('is_deleted', False) == True:
            raise exc.NotFoundError()
        return found_item

    def _transform_response(self, rows, totalCount):
        rows = [row.dict() for row in rows]

        return BaseListResponse(rows = rows, totalCount =len(rows))


    def list(self, body, model = None):

        model = self.model if model is None else model
        filters = body.get('filters', {})

        wheres = filters.get('wheres', [])
        orders = filters.get('orders', [])
        
        query = self.db.query(model)
        if hasattr(model, 'is_deleted'):
            query = query.filter(getattr(model, 'is_deleted') == False)

        for where in wheres:
            query = query.filter(getattr(model, where['column']) == where['value'])

        for order in orders:
            query = query.order_by(getattr(model, order['column']).desc() if order['desc'] else getattr(model, order['column']).asc())

        rows = query.all()


        return self._transform_response(rows, len(rows))

    def delete(self, body, field='id', model = None):
        """Delete one item from specific table by given field key and value.

        Args:
            body (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.\n
            None if provided field is not found on model.
        """
        model = self.model if model is None else model
        if not hasattr(model, field):
            raise exc.NotFoundError(field=field)

        item_to_delete = self.get(body, field, model)
        if not item_to_delete:
            raise exc.NotFoundError(field=field)
        self.db.delete(item_to_delete)
        self.db.commit()
        return item_to_delete
    
    def _is_value_empty(self, value) -> bool:
        null_values = [None, '', 'null', 'None', b'']
        return value in null_values

    def _is_immutable_field(self, field) -> bool:
        immutable_fields = ['id', 'login']
        return field in immutable_fields
    
    def update(self, body, model = None):
        """Update one item from one specific table by given fields

        Args:
            body (schemas.RequestBodyOne) Request body

        Returns:
            Item in DB that was found in db.\n
        """
        model = self.model if model is None else model
        item_to_update = self.get(body, 'id', model)
        if not item_to_update:
            raise exc.NotFoundError()

        valid_values = {}

        body = body.dict() if hasattr(body, 'dict') else body

        for key, value in body.items():
            if not self._is_value_empty(value) and not self._is_immutable_field(key):
                # print(f'Updated field {key} with value = {value}')
                valid_values[key] = value
                # setattr(item_to_update, key, value)

        self.db.query(model).filter(getattr(model, 'id') == item_to_update.get('id')).update(
            valid_values
        )
        
        self.db.commit()
        self.db.refresh(item_to_update)
        
        return item_to_update

    def mark_deleted(self, body, field = 'id', restore = False, model = None):
        """Mark one item as deleted from specific table by given field key and value.

        Args:
            value (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.\n
            None if provided field is not found on model.
        """
        model = self.model if model is None else model
        if not hasattr(model, 'is_deleted'):
            print(f'{model} do not have `is_deleted` property')
            raise exc.InternalError()

        item_to_delete = self.get(body, field, model)
        if not item_to_delete:
            raise exc.NotFoundError(field=field)

        # setattr(item_to_delete, 'is_deleted', (not restore))
        self.db.query(model).filter(getattr(model, field) == item_to_delete.get(field)).update({'is_deleted': True})
        self.db.commit()
        self.db.refresh(item_to_delete)
        
        return item_to_delete
