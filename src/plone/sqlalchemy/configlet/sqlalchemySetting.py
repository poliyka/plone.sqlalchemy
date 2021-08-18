from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.sqlalchemy import _
from plone.z3cform import layout
from z3c.form import form
from zope import schema
from zope.interface import Interface


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
