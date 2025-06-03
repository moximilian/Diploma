from sqlite3 import IntegrityError
import models as m
import api.exceptions as exc
from schemas import BaseListResponse
from functools import wraps
import typing as t


class BaseCRUD():
    """BaseCRUD implements base common logic that can be used
    by all other CRUD classes.

    Args:
        db: SqlAlchemy Session instance
        model: SqlAlchemy orm default model
        joined_models: Optional list of models in which filters will work. Defaults to [model]
    """

    def __init__(self, db, model, joined_models = []):
        self.db = db
        self.model = model
        self.joined_models = [model] if len(joined_models) == 0 else joined_models

    def _save_to_db(self, item: t.Dict[str, t.Any]):
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

    def get_item(self, body, field='id', model=None) -> m.BaseModel:
        """Get one item from specific table by given field key and value.

        Args:
            value (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.
            None if provided field is not found on model.
        """
        model = self.model if model is None else model

        query = self.db.query(model)
        if isinstance(field, str):
            if not hasattr(model, field):
                raise exc.NotFoundError(message='No such field on model', field=field)
            value = body.get(field)
            if value is None:
                raise exc.NotFoundError(message='Value is null', field=field)
            found_item = query.filter(getattr(model, field) == value).first()
        elif isinstance(field, list):
            for field_item in field:
                if not hasattr(model, field_item):
                    raise exc.NotFoundError(message='No such field on model', field=field_item)
                value = body.get(field_item)
                if value is None: raise exc.NotFoundError(message='Value is null', field=field)
                query = query.filter(getattr(model, field_item) == value)
            found_item = query.first()

        return found_item

    def get(self, body, field='id', model=None):
        """Get one item from specific table by given field key and value.

        Args:
            value (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.
            None if provided field is not found on model.
        """
        return self._make_output([self.get_item(body, field, model)])[0]

    def _make_output(self, rows):
        return rows

    def _transform_response(self, rows):
        """Transform response into defined format.

        Args:
            rows (list): List of items to wrap

        Returns:
            schemas.BaseListResponse
            .. code-block:: json
            {
                "rows": [],
                "totalCount" : 0
            }
        """
        rows = self._make_output(rows)
        rows = [row.dict() if not isinstance(row, dict) else row for row in rows]
        return BaseListResponse(rows=rows, totalCount=len(rows))


    def _transform_boolean(self, where):
        if isinstance(where, dict) and where.get('value') and where.get('value') in ['false', 'true']:
            where['value'] = where['value'].lower() in ("yes", "true", "t", "1")
        return where
    
    def _get_column_from_joined_models(self, column_name):
        for model in self.joined_models:
            if hasattr(model, column_name):
                return getattr(model, column_name)
            if column_name in model.__table__.columns:
                return model.__table__.columns[column_name]
        raise ValueError(f"Column '{column_name}' not found in any of the provided models")

    def list(self, body, model=None):
        """Get one or multiple items in list representation:

        Args:
            body(schemas.RequestBodyList)
            .. code-block:: json
            {
                "filters": {
                    "wheres" : [
                        {
                            "column":column,
                            "condition": condition,
                            "value":value
                        }
                    ],
                    "orders": [
                        {
                            "column": column,
                            "desc": boolean
                        }
                    ],
                    "search" : search value @todo,
                    "page": integer @todo
                    "limit": integer @todo
                }
            }
            model (model): sqlalchemy model on which to perform queries.
                Defaults to None, uses one in defined in constructor

        Returns:
            response (schemas.BaseListResponse)
        """
        rows = self.get_items(body, model)
        return self._transform_response(rows)

    def get_items(self, body, model=None):
        model = self.model if model is None else model
        filters = body.get('filters', {})

        wheres = filters.get('wheres', [])
        orders = filters.get('orders', [])

        query = self.db.query(model)
        if hasattr(model, 'is_deleted'):
            query = query.filter(getattr(model, 'is_deleted') == False)
        query, wheres = self._make_custom_query(query, wheres)
        for where in wheres:
            condition = where.get('condition')
            where = self._transform_boolean(where)
            column = self._get_column_from_joined_models(where['column'])
            if condition == 'between':
                query = query.filter(column.between(*where['value']))
            elif condition == '!=':
                query = query.filter(column != where['value'])
            elif condition == 'in':
                query = query.filter(column.in_(where['value']))
            elif condition == '%':
                query = query.filter(column.contains(where['value']))
            else:
                query = query.filter(column == where['value'])
        for order in orders:
            query = query.order_by(getattr(model, order['column']).desc(
            ) if order['desc'] else getattr(model, order['column']).asc())

        print(query.statement.compile())
        
        return query.all()

    def _make_custom_query(self, query, wheres):
        return query, wheres

    def _delete_item(self, body, field, model=None):
        item_to_delete = self.get_item(body, field, model)
        if not item_to_delete:
            raise exc.NotFoundError(field=field)
        self.db.delete(item_to_delete)
        self.db.commit()
        return item_to_delete

    def delete(self, body, field='id', model=None):
        """Delete one item from specific table by given field key and value.

        Args:
            body (RequestBodyOne or RequestBodyOnes) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'
            model (model): sqlalchemy model on which to perform queries.
                Defaults to None, uses one in defined in constructor

        Returns:
            Item in DB that was found in db.
            None if provided field is not found on model.
        """
        model = self.model if model is None else model
        if not hasattr(model, field):
            raise exc.NotFoundError(field=field)
        if body.get('ids') and isinstance(body.get('ids'), list):
            items_to_delete = []
            for item in body.get('ids'):
                item_to_delete = self._delete_item({'id': item}, field, model)
                items_to_delete.append(item_to_delete)
            return items_to_delete
        else: return self._delete_item(body, field, model)

    def _is_value_empty(self, value) -> bool:
        null_values = ['', 'null', 'None', b'']
        return value in null_values

    def _is_immutable_field(self, field) -> bool:
        immutable_fields = ['id', 'login']
        return field in immutable_fields

    def update(self, body, model=None):
        """Update one item from one specific table by given fields

        Args:
            body (schemas.RequestBodyOne) Request body
            model (model): sqlalchemy model on which to perform queries.
                Defaults to None, uses one in defined in constructor

        Returns:
            Item in DB that was found in db.
        """
        model = self.model if model is None else model
        item_to_update = self.get_item(body, 'id', model)
        if not item_to_update:
            raise exc.NotFoundError()

        valid_values = {}

        body = body.dict() if hasattr(body, 'dict') else body

        for key, value in body.items():
            if self._is_value_empty(value) or self._is_immutable_field(key):
                continue
            valid_values[key] = value

        self.db.query(model).filter(getattr(model, 'id') == item_to_update.get('id')).update(
            valid_values
        )

        self.db.commit()
        self.db.refresh(item_to_update)

        return item_to_update

    def mark_deleted(self, body, field='id', restore=False, model=None):
        """Mark one item as deleted from specific table by given field key and value.

        Args:
            value (schemas.RequestBodyOne) Request body
            field (str): Field key of model of which type is searched. Defaults to 'id'
            restore (bool): Flag by which item can be marked or restored. Defaults to False.as_integer_ratio
            model (model): sqlalchemy model on which to perform queries.
                Defaults to None, uses one in defined in constructor

        Returns:
            Item in DB that was found in db.
            None if provided field is not found on model.
        """
        model = self.model if model is None else model
        if not hasattr(model, 'is_deleted'):
            print(f'{model} do not have `is_deleted` property')
            raise exc.InternalError()

        item_to_delete = self.get_item(body, field, model)
        if not item_to_delete:
            raise exc.NotFoundError(field=field)

        # setattr(item_to_delete, 'is_deleted', (not restore))
        self.db.query(model).filter(getattr(model, field) == item_to_delete.get(
            field)).update({'is_deleted': (not restore)})
        self.db.commit()
        self.db.refresh(item_to_delete)

        return item_to_delete

    def insert(self, request_body, model=None) -> dict:
        model = self.model if model is None else model
        if not isinstance(request_body, list):
            request_body = [request_body]
        inserted_items = [
            model(
                **{
                    k: v for k, v in (item.items() if isinstance(item, dict) else item.model_dump().items()) if k in model.__table__.columns
                }
            ) for item in request_body
        ]
        created_items = []
        for item in inserted_items:
            created_items.append(self._save_to_db(item))
        return created_items
