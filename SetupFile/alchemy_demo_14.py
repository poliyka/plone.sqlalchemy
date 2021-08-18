# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

from plone.sqlalachemy.engine import Engine
from my.package.models.user import User, Address
from my.package.models.store import Store, Tag
from sqlalchemy.orm import aliased
import sqlalchemy as sa


class Test(BrowserView):
    def get_db_and_session(self):
        engine = Engine()
        return engine.db_session()

    def insert_data(self, session):
        ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")
        session.add(ed_user)
        session.add_all(
            [
                User(name="wendy", fullname="Wendy Williams", nickname="windy"),
                User(name="mary", fullname="Mary Contrary", nickname="mary"),
                User(name="fred", fullname="Fred Flintstone", nickname="freddy"),
            ]
        )
        session.commit()

        session.rollback()

    def update_data(self, session):
        # multiple
        session.query(User).filter(User.name == "ed").update(
            {
                "fullname": "ed Andy",
            }
        )
        session.commit()

        # single
        ed_user = session.query(User).filter(User.name == "ed").first()
        ed_user.fullname = "Ed test"
        session.commit()

        session.rollback()

    def delete_data(self, session):
        # multiple
        try:
            session.query(User).filter(User.name == "ed").delete()
            session.commit()
        except:
            session.rollback()

        # single
        try:
            wendy_user = session.query(User).filter(User.name == "wendy").first()
            session.delete(wendy_user)
            session.commit()
        except:
            session.rollback()

        session.rollback()

    def base_use(self, db):
        with db.connect() as conn:
            sqlString = "select name from users"
            result = conn.execute(sqlString)
            for row in result:
                print("name:", row["name"])

    def session_search(self, session):
        for instance in session.query(User).order_by(User.id):
            print(instance.name, instance.fullname)

        for row in session.query(User, User.name).all():
            print(row.User, row.name)

        for row in session.query(User.name.label("name_label")).all():
            print(row.name_label)

        session.rollback()

    def aliased_search(self, session):
        user_alias = aliased(User, name="user_alias")
        for row in session.query(user_alias, user_alias.name).all():
            print(row.user_alias)

        session.rollback()

    def query_filter(self, session):
        for (name,) in session.query(User.name).filter(User.fullname == "Ed Jones"):
            print(name)

        # *Reference https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping
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
        session.query(User).filter(User.name == "ed").filter(
            User.fullname == "Ed Jones"
        )

        # OR:
        from sqlalchemy import or_

        session.query(User).filter(or_(User.name == "ed", User.name == "wendy"))

        # limit
        session.query(User).filter(User.name != "ed").limit(1)

        # ColumnOperators.match():
        session.query(User).filter(User.name.match("wendy"))
        # Query.all() returns a list:
        user_filter = (
            session.query(User).filter(User.name.like("%e23d")).order_by(User.id)
        )
        user_filter.all()
        # Query.first() applies a limit of one and returns the first result as a scalar:
        user_filter.first()
        # Using Textual SQL
        from sqlalchemy import text

        for user in (
            session.query(User).filter(text("id<224")).order_by(text("id")).all()
        ):
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

        session.rollback()

    def many_to_one(self, session):
        first_store = Store(store_id=791215, store_name="Pallas", store_area="Taiwan")
        session.add(first_store)
        session.commit()
        user = session.query(User).first()
        store = session.query(Store).first()
        user.stores = [store]
        session.commit()

        session.rollback()

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
        session.commit()

        users = session.query(User).all()
        users[0].tag_rel = [tag1, tag2]
        users[1].tag_rel = [tag1]
        users[2].tag_rel = [tag1, tag3]
        session.commit()

        session.rollback()

        # print It
        users = session.query(User).all()
        result = []
        for user in users:
            result.append(user.tag_rel)
        print(result)

    def one_to_many(self, session):
        store = Store(store_id=101, store_name="店1", store_area="北")
        address = Address(address="Address")

        session.add_all(
            [
                store,
                address,
            ]
        )
        session.commit()
        user = session.query(User).first()
        address.users = user
        store.users = user
        session.commit()

        session.rollback()

    def one_to_one(self, session):
        store = session.query(Store).filter(Store.store_id == 101).one_or_none()
        address = session.query(Address).first()
        address.stores = store
        session.commit()

        session.rollback()

    def __call__(self):
        """
        類似Django ORM的使用方式
        https://github.com/absent1706/sqlalchemy-mixins
        """
        request = self.request
        portal = api.portal.get()
        db, session = self.get_db_and_session()

        # https://docs.sqlalchemy.org/en/13/core/dml.html
        # *Demo function
        self.insert_data(session)
        # self.update_data(session)
        # self.delete_data(session)
        # self.base_use(db)
        # self.session_search(session)
        # self.aliased_search(session)
        # self.query_filter(session)
        # self.many_to_one(session)
        # self.many_to_many(session)
        # self.one_to_many(session)
        # self.one_to_one(session)

        session.close()
        return "Test done"
