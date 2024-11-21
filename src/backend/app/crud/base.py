import models as m


class BaseCRUD():
    """BaseCRUD implements base common logic that can be used
    by all other CRUD classes.

    Args:
        db: SqlAlchemy Session instance
    """

    def __init__(self, db):
        self.db = db

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

    def _get_item_by_field(self, model: m.BaseModel, value, field='id'):
        """Get one item from specific table by given field key and value.

        Args:
            model (m.BaseModel ->()): Model corresponding to table in which search will be executed.
            value (Any): Unique value by which filter will apply
            field (str): Field key of model of which type is searched. Defaults to 'id'

        Returns:
            Item in DB that was found in db.\n
            None if provided field is not found on model.
        """
        if not hasattr(model, field):
            return None
        return self.db.query(model).filter(model[field] == value).first()
