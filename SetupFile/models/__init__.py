from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import os

class AlembicNotFoundError(Exception):
    pass

class SqlalchemyUrlEmpty(Exception):
    pass


Base = declarative_base()

class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True



CURRENT_DIR = os.path.dirname(__file__)
alembic_path = os.path.abspath(CURRENT_DIR + '/../alembic.ini')
config = configparser.ConfigParser()
config.read(alembic_path)

if not config:
    raise AlembicNotFoundError("File: [alembic.ini] not found! Please check your file path.")

sqlString = config.get('alembic', 'sqlalchemy.url')
if not sqlString:
    raise SqlalchemyUrlEmpty("[alembic] sqlalchemy.url not have value!")

db = create_engine(sqlString, echo=True)
session = sessionmaker(bind=db)

BaseModel.set_session(session())
