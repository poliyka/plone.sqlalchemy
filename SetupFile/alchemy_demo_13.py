# -*- coding: utf-8 -*-
from learn.plone import _
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.sqlalchemy.engine import Engine
from learn.plone.models.user import User, Address
from learn.plone.models.store import Store, Tag

from sqlalchemy.orm import aliased
from sqlalchemy import select, insert, update, delete
import sqlalchemy as sa

import threading
import transaction
from pprint import pprint


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
    def insert_data(self, session):
        # 2.0
        stmt = insert(User).values(name="new", fullname="hello", nickname="world")
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
            update(User)
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
        stmt = select([User.age], User.name == "new")
        age = session.execute(stmt).scalars().first()
        printC("age: " + str(age))
        stmt = (
            update(User)
            .where(User.name == "new")
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
        printC(session.execute(select(User)).scalars().all())

        # Get in id
        user = session.get(User, 5)

        # query in ids
        stmt = select([User.name], User.id.in_([1, 2, 3, 4]))
        printC(session.execute(stmt).scalars().all())

        # list emits a deprecation warning
        stmt = select([User.name, User.identity])

        # Return the first element.
        printC(session.execute(stmt).scalars().all())

        # Return all element.
        printC(session.execute(stmt).mappings().all())

        # Use case set new label
        case_clause = sa.case(
            [(User.id == 3, "three"), (User.id == 7, "seven")],
            else_="neither three nor seven",
        ).label("newLabel")
        stmt = select(User, case_clause)
        printC(session.execute(stmt).mappings().all())

    def __call__(self):
        """
        1.0 與 2.0 使用ORM方式的差異
        https://docs.sqlalchemy.org/en/14/changelog/migration_20.html#migration-orm-usage
        類似sqlalchemy-mixins的使用方式
        https://github.com/absent1706/sqlalchemy-mixins
        """

        engine = Engine()
        session = engine.Session()

        # self.insert_data(engine.session)
        # self.update_data(engine.session)
        for i in range(200):
            self.transaction_data(session)

        # self.select_data(engine.session)
        # self.delete_data(engine.session)
        # self.base_use(engine.db)
        # self.session_search(engine.session)
        # self.aliased_search(engine.session)
        # self.query_filter(engine.session)
        # self.many_to_one(engine.session)
        # self.many_to_many(engine.session)
        # self.one_to_many(engine.session)
        # self.one_to_one(engine.session)
        session.close()
        return "done"
