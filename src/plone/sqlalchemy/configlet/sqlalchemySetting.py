from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout
from z3c.form import form
from zope.interface import Interface
from zope import schema

from plone.sqlalchemy import _


class ISiteSetting(Interface):

    db_string = schema.TextLine(
        title=_(u"database path"),
        description=_(u"https://docs.sqlalchemy.org/en/14/core/connections.html#basic-usage"),
        required=False,
    )


class SiteSettingControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ISiteSetting


SiteSettingControlPanelView = layout.wrap_form(SiteSettingControlPanelForm, ControlPanelFormWrapper)
SiteSettingControlPanelView.label = _(u"Sqlalchemy Settings")
