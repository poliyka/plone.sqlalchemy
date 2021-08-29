import sqlalchemy as sa
from sqlalchemy.orm import relationship
from my.package.models import BaseModel


class Store(BaseModel):
    __tablename__ = "stores"
    __repr_attrs__ = ["id", "store_name"]

    store_id = sa.Column(sa.Integer, unique=True)
    store_name = sa.Column(sa.String(128), nullable=False)
    store_area = sa.Column(sa.String(128), nullable=True)
    create_time = sa.Column(sa.DateTime, server_default=sa.text("NOW()"))
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"))
    # one to one Use uselist=False
    address_ids = relationship("user.Address", uselist=False, backref="stores", lazy=True)


class Tag(BaseModel):
    __tablename__ = "tags"
    __repr_attrs__ = ["id", "tag_type"]

    tag_type = sa.Column(sa.String(30))
    insert_time = sa.Column(sa.DateTime, server_default=sa.text("NOW()"))
    update_time = sa.Column(sa.DateTime, onupdate=sa.text("NOW()"), server_default=sa.text("NOW()"))
