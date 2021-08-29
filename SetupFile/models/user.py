import sqlalchemy as sa
from sqlalchemy.orm import relationship
from my.package.models import BaseModel


user_to_tag = sa.Table(
    "user_to_tag",
    BaseModel.metadata,
    sa.Column("tag_id", sa.Integer, sa.ForeignKey("tags.id")),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("other_field", sa.String(30)),
    extend_existing=True,
)


class User(BaseModel):
    __tablename__ = "users"
    __repr_attrs__ = ["name", "fullname"]

    name = sa.Column(sa.String(128))
    identity = sa.Column(sa.String(64), unique=True)
    age = sa.Column(sa.Integer(), default=0)
    fullname = sa.Column(sa.String(128))
    nickname = sa.Column(sa.String(128))
    address_ids = relationship("user.Address", uselist=True, backref="users", lazy=True)
    store_ids = relationship("store.Store", uselist=True, backref="users", lazy=True)
    tag_ids = relationship("store.Tag", secondary=user_to_tag, backref="users", lazy=True)

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

# event
@sa.event.listens_for(User, "before_insert")
def receive_before_insert(mapper, connection, target):
    "listen for the 'before_insert' event"


@sa.event.listens_for(User, "after_insert")
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"


@sa.event.listens_for(User, "before_update")
def receive_before_update(mapper, connection, target):
    "listen for the 'before_update' event"


@sa.event.listens_for(User, "after_update")
def receive_after_update(mapper, connection, target):
    "listen for the 'after_update' event"



class Address(BaseModel):
    __tablename__ = "address"
    __repr_attrs__ = ["address"]

    address = sa.Column(sa.String(128), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"))
    store_id = sa.Column(sa.Integer, sa.ForeignKey("stores.id", ondelete="SET NULL"))
