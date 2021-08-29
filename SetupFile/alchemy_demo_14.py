# -*- coding: utf-8 -*-
import random
from pprint import pprint

import sqlalchemy as sa
import transaction
from plone import api
from plone.sqlalchemy.engine import Engine
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sqlalchemy.orm import aliased

from learn.plone import _
from learn.plone.models.store import Store, Tag
from learn.plone.models.user import Address, User

# import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)


def printR(word):
    print("\033[91m", end="")
    pprint(word)
    print("\033[0m", end="")


def printG(word):
    print("\033[92m", end="")
    pprint(word)
    print("\033[0m", end="")


def printY(word):
    print("\033[93m", end="")
    pprint(word)
    print("\033[0m", end="")


def printB(word):
    print("\033[94m", end="")
    pprint(word)
    print("\033[0m", end="")


def printP(word):
    print("\033[95m", end="")
    pprint(word)
    print("\033[0m", end="")


def printC(word):
    print("\033[96m", end="")
    pprint(word)
    print("\033[0m", end="")


class Alchemy(BrowserView):
    def show_engine_args(self, engine):
        printC(engine.engine_args)

    def insert_data(self, session):
        # 2.0
        stmt = sa.insert(User).values(name="new", fullname="hello", nickname="world")
        session.execute(stmt)

        # 1.0
        ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")
        session.add(ed_user)
        session.add_all(
            [
                User(name="wendy", fullname="Wendy Williams", nickname="windy"),
                User(name="mary", fullname="Mary Contrary", nickname="mary"),
                User(name="fred", fullname="Fred Flintstone", nickname="freddy"),
            ]
        )

        transaction.commit()

    def update_data(self, session):
        # 2.0
        # multiple
        stmt = (
            sa.update(User)
            .where(User.name == "new")
            .values(
                {
                    "fullname": "update_name",
                }
            )
        )

        session.execute(stmt)

        # 1.0
        # multiple
        session.query(User).filter(User.name == "ed").update(
            {
                "fullname": "ed Andy",
            }
        )
        transaction.commit()

        # single
        ed_user = session.query(User).filter(User.name == "ed").first()
        ed_user.fullname = "Ed test"

        transaction.commit()

    def transaction_data(self, session):
        printC("transaction_data")
        stmt = sa.select([User.age], User.name == "wendy")
        age = session.execute(stmt).scalars().first()
        printC("age: " + str(age))
        stmt = (
            sa.update(User)
            .where(User.name == "wendy")
            .values(
                {
                    "age": age + 1,
                }
            )
        )

        session.execute(stmt)
        transaction.commit()

    def select_data(self, session):
        # Get all User Object
        printC(session.execute(sa.select(User)).scalars().all())

        # query in ids
        stmt = sa.select([User.name], User.id.in_([1, 2, 3, 4]))
        printC(session.execute(stmt).scalars().all())

        # list emits a deprecation warning
        stmt = sa.select([User.name, User.identity])

        # Return the first element.
        printC(session.execute(stmt).scalars().all())

        # Return all element.
        printC(session.execute(stmt).mappings().all())

        # Use case set new label
        case_clause = sa.case(
            [(User.id == 3, "three"), (User.id == 7, "seven")],
            else_="neither three nor seven",
        ).label("newLabel")
        stmt = sa.select(User, case_clause)
        printC(session.execute(stmt).mappings().all())

    def delete_data(self, session):
        # 2.0
        # multiple
        stmt = sa.delete(User).where(User.name == "new")
        session.execute(stmt)
        transaction.commit()

        # 1.0
        # multiple
        # session.query(User).filter(User.name == "ed").delete()
        # session.commit()

        # single
        # wendy_user = session.query(User).filter(User.name == "wendy").first()
        # session.delete(wendy_user)
        # session.commit()

    def base_use(self, db):
        with db.connect() as conn:
            stmt = sa.text("SELECT * FROM users")
            result = conn.execute(stmt)
            for row in result:
                printC(f"name: {row['name']}")

    def session_search(self, session):
        for row in session.query(User).order_by(User.id):
            printC(f"name: {row.name}, fullname: {row.fullname}")

        for row in session.query(User, User.name).all():
            printC(f"Obj: {row.User}, name: {row.name}")

        for row in session.query(User.name.label("name_label")).all():
            printC(f"name_label: {row.name_label}")

    def aliased_search(self, session):
        user_alias = aliased(User, name="user_alias")
        for row in session.query(user_alias, user_alias.name).all():
            print(row.user_alias)

    def query_filter(self, session):
        for (name,) in session.query(User.name).filter(User.fullname == "Ed Jones"):
            print(name)

        # *Reference https://docs.sqlalchemy.org/en/14/orm/tutorial.html#declare-a-mapping
        # ColumnOperators.__eq__():
        session.query(User).filter(User.name == "ed")
        # ColumnOperators.__ne__():
        session.query(User).filter(User.name != "ed")
        # ColumnOperators.like():
        session.query(User).filter(User.name.like("%ed%"))
        # ColumnOperators.ilike() (case-insensitive LIKE):
        session.query(User).filter(User.name.ilike("%ed%"))
        # ColumnOperators.in_():
        session.query(User).filter(User.name.in_(["ed", "wendy", "jack"]))
        # ColumnOperators.notin_():
        session.query(User).filter(~User.name.in_(["ed", "wendy", "jack"]))

        # ColumnOperators.is_():
        session.query(User).filter(User.name == None)
        #! alternatively, if pep8/linters are a concern
        # session.query(User).filter(User.name.is_(None))

        # ColumnOperators.isnot():
        session.query(User).filter(User.name != None)
        #! alternatively, if pep8/linters are a concern
        # session.query(User).filter(User.name.isnot(None))

        # AND:
        # use and_()
        from sqlalchemy import and_

        session.query(User).filter(and_(User.name == "ed", User.fullname == "Ed Jones"))
        #! or send multiple expressions to .filter()
        session.query(User).filter(User.name == "ed", User.fullname == "Ed Jones")
        #! or chain multiple filter()/filter_by() calls
        session.query(User).filter(User.name == "ed").filter(User.fullname == "Ed Jones")

        # OR:
        from sqlalchemy import or_

        session.query(User).filter(or_(User.name == "ed", User.name == "wendy"))

        # limit
        session.query(User).filter(User.name != "ed").limit(1)

        # ColumnOperators.match():
        session.query(User).filter(User.name.match("wendy"))
        # Query.all() returns a list:
        user_filter = session.query(User).filter(User.name.like("%e23d")).order_by(User.id)
        user_filter.all()
        # Query.first() applies a limit of one and returns the first result as a scalar:
        user_filter.first()
        # Using Textual SQL
        from sqlalchemy import text

        for user in session.query(User).filter(text("id<224")).order_by(text("id")).all():
            print(user.name)

        # Bind parameters can be specified with string-based SQL, using a colon. To specify the values, use the Query.params() method:
        session.query(User).filter(text("id<:value and name=:name")).params(
            value=224, name="fred"
        ).order_by(User.id).one()

        # Count
        count = session.query(sa.func.count(User.id)).all()
        print(count)
        # distinct
        distinct = session.query(sa.func.distinct(User.name)).all()
        print(distinct)

    def many_to_one(self, session):
        first_store = Store(
            store_id=random.randint(1, 100), store_name="Pallas", store_area="Taiwan"
        )
        session.add(first_store)
        transaction.commit()

        user = session.query(User).first()
        stores = session.query(Store).all()
        user.store_ids = stores
        transaction.commit()

    def many_to_many(self, session):
        tag1 = Tag(tag_type="Apple")
        tag2 = Tag(tag_type="Orange")
        tag3 = Tag(tag_type="Berry")

        session.add_all(
            [
                tag1,
                tag2,
                tag3,
            ]
        )
        transaction.commit()

        users = session.query(User).all()
        users[0].tag_ids = [tag1, tag2]
        users[1].tag_ids = [tag1]
        users[2].tag_ids = [tag1, tag3]
        transaction.commit()

        # print It
        users = session.query(User).all()
        result = []
        for user in users:
            result.append(user.tag_ids)
        printC(result)

    def one_to_many(self, session):
        store = Store(store_id=101, store_name="店1", store_area="北")
        address = Address(address="Address")

        session.add_all(
            [
                store,
                address,
            ]
        )
        transaction.commit()

        user = session.query(User).first()
        address.users = user
        store.users = user
        transaction.commit()

    def one_to_one(self, session):
        store = session.query(Store).filter(Store.store_id == 101).one_or_none()
        Address.create(address="Address")
        address = session.query(Address).first()
        address.store_id = store.id
        transaction.commit()

    def __call__(self):
        """
        1.0 與 2.0 使用ORM方式的差異
        https://docs.sqlalchemy.org/en/14/changelog/migration_20.html#migration-orm-usage
        類似sqlalchemy-mixins的使用方式
        https://github.com/absent1706/sqlalchemy-mixins
        """

        execution_options = {"isolation_level": "READ UNCOMMITTED", "logging_token": "Normal"}
        engine = Engine(echo=True, execution_options=execution_options)
        session = engine.Session()

        self.insert_data(session)
        # self.update_data(session)
        # for i in range(200):
        #     self.transaction_data(session)
        # self.select_data(session)
        # self.delete_data(session)
        # self.base_use(engine.db)
        # self.session_search(session)
        # self.aliased_search(session)
        # self.query_filter(session)
        # self.many_to_one(session)
        # self.many_to_many(session)
        # self.one_to_many(session)
        # self.one_to_one(session)
        session.close()
        return "done"
