# -*- coding: utf-8 -*-
from collective.soundcloud import _
from collective.soundcloud import _p
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform.directives import omitted
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from soundcloudapi import AuthInfo
from soundcloudapi import SoundcloudException
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.component import getUtility
from zope.interface import Interface
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class ISettings(Interface):
    ' Define settings data structure '

    client_id = schema.TextLine(
        title=_(u'Client ID'),
        description=_(u'OAuth 2 Client Id'),
        required=True,
    )

    client_secret = schema.TextLine(
        title=_(u'Client Secret'),
        description=_(u'OAuth 2 Client Secret'),
        required=True,
    )

    omitted('token')
    token = schema.TextLine(
        title=_(u'Token'),
        description=_(u'Soundcloud Token'),
        required=False,
    )


def get_soundcloud_settings():
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISettings)
    return settings


def _get_auth_info(client_id, client_secret, context):
    return AuthInfo(
        client_id,
        client_secret,
        redirect_uri='{0}/soundcloud_redirect_handler'.format(
            context.absolute_url()
        )
    )


class SettingsEditForm(RegistryEditForm):
    """ Define form logic
    """
    form.extends(RegistryEditForm)
    schema = ISettings
    label = _(u'Soundcloud Settings')

    @button.buttonAndHandler(_p(u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        settings = get_soundcloud_settings()
        if (
            data.get('client_id') == settings.client_id and
            data.get('client_secret') == settings.client_secret and
            settings.token
        ):
            IStatusMessage(self.request).addStatusMessage(
                _(u'All values unchanged.'),
                "info"
            )
            self.request.response.redirect(self.request.getURL())
            return
        authinfo = _get_auth_info(
            data.get('client_id'),
            data.get('client_secret'),
            self.context
        )
        self.applyChanges(data)
        self.request.RESPONSE.redirect(authinfo.redirect_url)


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)


class SoundcloudRedirectHandler(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.request.RESPONSE.redirect(
            '{0}/soundcloud-settings'.format(self.context.absolute_url())
        )
        code = self.request.form.get('code')
        if not code:
            IStatusMessage(self.request).addStatusMessage(
                _(u'Soundcloud code not fetched.'),
                "error"
            )
            return
        settings = get_soundcloud_settings()
        authinfo = _get_auth_info(
            settings.client_id,
            settings.client_secret,
            self.context
        )
        try:
            authinfo.token_from_code(code)
        except SoundcloudException:
            IStatusMessage(self.request).addStatusMessage(
                _(u'Soundcloud can not transform code to token.'),
                "error"
            )
            return
        settings.token = authinfo.token
        IStatusMessage(self.request).addStatusMessage(
            _(u'Soundcloud settings completed and saved.'),
            "info"
        )
