# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import plone.sqlalchemy


class PloneSqlalchemyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plone.sqlalchemy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.sqlalchemy:default')


PLONE_SQLALCHEMY_FIXTURE = PloneSqlalchemyLayer()


PLONE_SQLALCHEMY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_SQLALCHEMY_FIXTURE,),
    name='PloneSqlalchemyLayer:IntegrationTesting',
)


PLONE_SQLALCHEMY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_SQLALCHEMY_FIXTURE,),
    name='PloneSqlalchemyLayer:FunctionalTesting',
)


PLONE_SQLALCHEMY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE_SQLALCHEMY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PloneSqlalchemyLayer:AcceptanceTesting',
)
