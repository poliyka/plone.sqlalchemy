from plone import api
from plone.sqlalchemy.configlet.sqlalchemySetting import ISiteSetting
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register
from typing import TypeVar, Iterable, Tuple, List, Dict, Mapping, Set, Union, Any


class DBStringNotExistException(Exception):
    """db_string not exist exception"""


class Engine:
    def __init__(
        self,
        db_string: str = None,
        echo: Union[Any, bool] = False,
        echo_pool: Union[str, bool] = False,
        encoding: str = "utf-8",
        connect_args: dict = {},
        execution_options: dict = {},
        autocommit: bool = False,
    ):
        """
        param echo: Log query 資訊 (True, False, 'debug')
        param echo_pool: Log 級別 (True, False, 'debug')
        param execution_options:
            "isolation_level": "READ UNCOMMITTED"
            "logging_token": "track1"
            "autocommit"= True

        param connect_args:
            在mysql使用 show variables; 可以查看可使用參數,常用的有以下參數
            {"charset": "utf8mb4", "connect_timeout": 10}

        摘要:[SQL] 使用 交易隔離等級 鎖定 Table 動作
            隔離層級分為四種
            READ UNCOMMITTED : 完全沒有隔離效果，可能讀取其他交易進行中尚未被COMMIT的資料。
            READ COMMITTED : 不允許讀取尚未COMMIT的資料，因為尚未被COMMITTED的資料可能隨時會再變。
            REPEATABLE READ : 在查詢中所讀取的資料會被鎖定，以免被其他使用者更改或刪除，以保證在交易中每次都可以讀到相同的資料。但是，仍然允許其他使用者對資料表的新增資料作業。
            SERIALIZABLE : 在查詢中所讀取的資料會被鎖定，以免被其他使用者更改或刪除，以保證在交易中每次都可以讀到相同的資料。但是，仍然允許其他使用者對資料表的新增資料作業。
            AUTOCOMMIT: 自動commit
        """

        if not db_string:
            self.db_string = api.portal.get_registry_record("db_string", interface=ISiteSetting)
        else:
            self.db_string = db_string
        if not self.db_string:
            raise DBStringNotExistException("db_string not exist")

        self._db = self._create_engine(echo, echo_pool, encoding, connect_args)
        self._Session = scoped_session(
            sessionmaker(
                bind=self._db.execution_options(**execution_options), autocommit=autocommit
            )
        )
        register(self._Session)

    def _create_engine(self, echo, echo_pool, encoding, connect_args):
        kwargs = {
            "future": True,
            "echo": echo,
            "echo_pool": echo_pool,
            "encoding": encoding,
        }
        if connect_args:
            kwargs.setdefault("connect_args", connect_args)

        return create_engine(self.db_string, **kwargs)

    @property
    def db(self):
        return self._db

    @property
    def Session(self):
        return self._Session

    @property
    def engine_args(self):
        args, kwargs = self._db.dialect.create_connect_args(self._db.url)
        return args, kwargs

    @property
    def version(self):
        import sqlalchemy

        return sqlalchemy.__version__
