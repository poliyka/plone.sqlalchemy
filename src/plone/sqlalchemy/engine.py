from plone import api
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from plone.sqlalchemy.configlet.sqlalchemySetting import ISiteSetting

import contextlib

class DBStringNotExistException(Exception):
    """db_string not exist exception"""

class Engine:
    def __init__(self, db_string=None):
        if not db_string:
            self.db_string = api.portal.get_registry_record("db_string", interface=ISiteSetting)
        else:
            self.db_string = db_string
        if not self.db_string:
            raise DBStringNotExistException("db_string not exist")

        self.db = self._create_engine()
        self.Session = sessionmaker(bind=self.db)

    def _create_engine(self):
        return create_engine(self.db_string, echo=True, future=True)

    @contextlib.contextmanager
    def transaction(self, connection):
        if not connection.in_transaction():
            with connection.begin():
                yield connection
        else:
            yield connection
