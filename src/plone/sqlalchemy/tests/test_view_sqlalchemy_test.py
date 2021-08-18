# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.sqlalchemy.testing import (
    PLONE_SQLALCHEMY_FUNCTIONAL_TESTING,
    PLONE_SQLALCHEMY_INTEGRATION_TESTING,
)
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = PLONE_SQLALCHEMY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_sqlalchemy_test_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='sqlalchemy-test'
        )
        self.assertTrue(view.__name__ == 'sqlalchemy-test')
        # self.assertTrue(
        #     'Sample View' in view(),
        #     'Sample View is not found in sqlalchemy-test'
        # )

    def test_sqlalchemy_test_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='sqlalchemy-test'
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = PLONE_SQLALCHEMY_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
