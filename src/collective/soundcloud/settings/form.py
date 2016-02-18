# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
from zExceptions import Unauthorized
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five import BrowserView
import yafowil.loader
from yafowil.base import UNSET
from yafowil.controller import Controller
from yafowil.yaml import parse_from_YAML
from soundcloudapi import AuthInfo
from soundcloudapi import SoundcloudException
from collective.soundcloud.settings import get_soundcloud_settings

_ = MessageFactory('collective.soundcloud')


class SoundcloudViewMixin(object):

    @property
    def controlpanel_uri(self):
        return '%s/soundcloud_controlpanel' % self.context.absolute_url()

    @property
    def redirect_uri(self):
        return '%s/soundcloud_redirect_handler' % self.context.absolute_url()

    @property
    def settings(self):
        return get_soundcloud_settings()

    @property
    def messages(self):
        return IStatusMessage(self.request)


class SoundcloudControlPanel(SoundcloudViewMixin, BrowserView):

    def form(self):
        form = parse_from_YAML('collective.soundcloud.settings:form.yaml',
                               self, _)
        self.redirected = False
        controller = Controller(form, self.request)
        if not controller.next:
            return controller.rendered
        if not self.redirected:
            self.request.RESPONSE.redirect(self.action)
        return u''

    def next(self, request):
        return self.controlpanel_uri

    @property
    def action(self):
        return self.controlpanel_uri

    def save(self, widget, data):
        if self.request.method != 'POST':
            raise Unauthorized('POST only')
        newid = data['client_id'].extracted
        newsec = data['client_secret'].extracted
        if self.settings.client_id == newid \
           and self.settings.client_secret == newsec \
           and self.settings.token:
            self.messages.addStatusMessage(_(u'All values unchanged.'),
                                           type="info")
            return
        self.settings.client_id = newid
        self.settings.client_secret = newsec
        authinfo = AuthInfo(newid, newsec, redirect_uri=self.redirect_uri)
        self.redirected = True
        self.request.RESPONSE.redirect(authinfo.redirect_url)


class SoundcloudRedirectHandler(SoundcloudViewMixin, BrowserView):

    def __call__(self):
        self.request.RESPONSE.redirect(self.controlpanel_uri)
        code = self.request.form.get('code')
        if not code:
            self.messages.addStatusMessage(_(u'Soundcloud code not fetched.'),
                                           type="error")
            return
        authinfo = AuthInfo(self.settings.client_id,
                            self.settings.client_secret,
                            redirect_uri=self.redirect_uri)
        try:
            authinfo.token_from_code(code)
        except SoundcloudException as e:
            self.messages.addStatusMessage(
                _(u'Soundcloud can not transform code to token.'), type="error")
            return
        self.settings.token = authinfo.token
        self.messages.addStatusMessage(
            _(u'Soundcloud settings completed and saved.'), type="info")
