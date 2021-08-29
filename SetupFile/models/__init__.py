import configparser
import os

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_mixin, declared_attr, registry
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_mixins import AllFeaturesMixin


class AlembicNotFoundError(Exception):
    pass


class SqlalchemyUrlEmpty(Exception):
    pass


# registry
mapper_registry = registry()
Base = mapper_registry.generate_base()


# Mixin
@declarative_mixin
class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {"mysql_engine": "InnoDB"}
    __table_args__ = {"keep_existing": True}
    __mapper_args__ = {"always_refresh": True}
    id = sa.Column(sa.Integer, primary_key=True)


class BaseModel(Base, BaseMixin, AllFeaturesMixin):
    __abstract__ = True


# For using sqlalchemy-mixins
CURRENT_DIR = os.path.dirname(__file__)
alembic_path = os.path.abspath(CURRENT_DIR + "/../alembic.ini")
config = configparser.ConfigParser()
config.read(alembic_path)

if not config:
    raise AlembicNotFoundError("File: [alembic.ini] not found! Please check your file path.")

db_string = config.get("alembic", "sqlalchemy.url")
if not db_string:
    raise SqlalchemyUrlEmpty("[alembic] sqlalchemy.url not have value!")

execution_options = {"isolation_level": "READ UNCOMMITTED", "logging_token": "SqlalchemyMixin"}
engine = create_engine(db_string, echo=True, future=True)
Session = scoped_session(
    sessionmaker(
        bind=engine.execution_options(**execution_options), autocommit=True
    )
)
BaseModel.set_session(Session())

