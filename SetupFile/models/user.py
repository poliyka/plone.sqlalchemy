import sqlalchemy as sa
from sqlalchemy.orm import relationship
from mingtak.ORM.models import BaseModel
import enum


class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3


user_tag_rel = sa.Table(
    "user_tag_rel",
    BaseModel.metadata,
    sa.Column("tag_rt", sa.Integer, sa.ForeignKey("tags.id")),
    sa.Column("user_rt", sa.Integer, sa.ForeignKey("users.id")),
)


class User(BaseModel):
    __tablename__ = "users"
    __repr_attrs__ = ["name", "fullname"]

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128))
    fullname = sa.Column(sa.String(128))
    nickname = sa.Column(sa.String(128))
    addresses = relationship("Address", uselist=True, backref="users", lazy=True)
    stores = relationship("Store", uselist=True, backref="users", lazy=True)
    tag_rel = relationship("Tag", secondary=user_tag_rel, backref="users", lazy=True)

    # https://docs.sqlalchemy.org/en/13/core/type_basics.html
    # BigInteger = sa.Column(sa.BigInteger)
    # Boolean = sa.Column(sa.Boolean)
    # Date = sa.Column(sa.Date)
    # DateTime = sa.Column(sa.DateTime)
    # Enum = sa.Column(sa.Enum(MyEnum))
    # Float = sa.Column(sa.Float)
    # Integer = sa.Column(sa.Integer)
    # Interval = sa.Column(sa.Interval)
    # LargeBinary = sa.Column(sa.LargeBinary)
    # Numeric = sa.Column(sa.Numeric)
    # PickleType = sa.Column(sa.PickleType)
    # SmallInteger = sa.Column(sa.SmallInteger)
    # String = sa.Column(sa.String)
    # Text = sa.Column(sa.Text)
    # Time = sa.Column(sa.Time)
    # Unicode = sa.Column(sa.Unicode)
    # UnicodeText = sa.Column(sa.UnicodeText)


class Address(BaseModel):
    __tablename__ = "user_address"
    __repr_attrs__ = ["address"]

    id = sa.Column(sa.Integer, primary_key=True)
    address = sa.Column(sa.String(128), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"))
    store_id = sa.Column(sa.Integer, sa.ForeignKey("stores.id", ondelete="SET NULL"))

    def __init__(self, address):
        self.address = address
