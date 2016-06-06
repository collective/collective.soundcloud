# -*- coding: utf-8 -*-
from collective.soundcloud import _
from collective.soundcloud import _p
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform.directives import omitted
from plone.protect.interfaces import IDisableCSRFProtection
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import Interface

import requests
import soundcloud


class ISettings(Interface):
    ' Define settings data structure '

    client_id = schema.TextLine(
        title=_(u'Client ID'),
        description=_(
            u'OAuth 2 Client Id, see http://soundcloud.com/you/apps, '
            u'will be stored here.'
        ),
        required=True,
    )

    client_secret = schema.TextLine(
        title=_(u'Client Secret'),
        description=_(
            u'OAuth 2 Client Secret. '
            u'It does not get stored in the settings.'
        ),
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

        # something changed?
        settings = get_soundcloud_settings()
        if (data.get('client_id') == settings.client_id) and settings.token:
            IStatusMessage(self.request).addStatusMessage(
                _(u'All values unchanged.'),
                "info"
            )
            self.request.response.redirect(self.request.getURL())
            return

        # store data
        settings.client_id = data.get('client_id')
        settings.client_secret = data.get('client_secret')

        # handle soundcloud
        client = soundcloud.Client(
            client_id=data.get('client_id'),
            client_secret=data.get('client_secret'),
            redirect_uri='{0}/soundcloud_redirect_handler'.format(
                self.context.absolute_url()
            )
        )
        self.request.RESPONSE.redirect(client.authorize_url())


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
        client = soundcloud.Client(
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            redirect_uri='{0}/soundcloud_redirect_handler'.format(
                self.context.absolute_url()
            )
        )
        try:
            result = client.exchange_token(
                code=code
            )
        except requests.HTTPError as e:
            # no idea at the moment what this exception may be
            IStatusMessage(self.request).addStatusMessage(
                _(
                    u'Soundcloud can not transform code to token.: ' +
                    e.message
                ),
                "error"
            )
            return
        settings.token = result.obj['access_token']
        settings.client_secret = u'a token was stored'
        IStatusMessage(self.request).addStatusMessage(
            _(u'Soundcloud settings completed and saved.'),
            "info"
        )
