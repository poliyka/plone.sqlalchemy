from plone import api
from sqlalchemy import create_engine
from zope.sqlalchemy import register
from sqlalchemy.orm import sessionmaker, scoped_session

from plone.sqlalchemy.configlet.sqlalchemySetting import ISiteSetting

import contextlib


class DBStringNotExistException(Exception):
    """db_string not exist exception"""


class Engine:
    def __init__(self, db_string=None, session_level="READ UNCOMMITTED"):
        """
        摘要:[SQL] 使用 交易隔離等級 鎖定 Table 動作
            隔離層級分為四種
            READ UNCOMMITTED : 完全沒有隔離效果，可能讀取其他交易進行中尚未被COMMIT的資料。
            READ COMMITTED : 不允許讀取尚未COMMIT的資料，因為尚未被COMMITTED的資料可能隨時會再變。
            REPEATABLE READ : 在查詢中所讀取的資料會被鎖定，以免被其他使用者更改或刪除，以保證在交易中每次都可以讀到相同的資料。但是，仍然允許其他使用者對資料表的新增資料作業。
            SERIALIZABLE : 在查詢中所讀取的資料會被鎖定，以免被其他使用者更改或刪除，以保證在交易中每次都可以讀到相同的資料。但是，仍然允許其他使用者對資料表的新增資料作業。
        """

        if not db_string:
            self.db_string = api.portal.get_registry_record("db_string", interface=ISiteSetting)
        else:
            self.db_string = db_string
        if not self.db_string:
            raise DBStringNotExistException("db_string not exist")

        self.db = self._create_engine()
        self.Session = scoped_session(
            sessionmaker(bind=self.db.execution_options(isolation_level=session_level))
        )
        register(self.Session)

    def _create_engine(self):
        return create_engine(self.db_string, echo=True, future=True)

    @contextlib.contextmanager
    def transaction(self):
        print(f"=============={self.session.get_transaction()}===============")
        if not self.session.get_transaction():
            with self.session.begin() as session:
                yield session
        else:
            yield self.session
