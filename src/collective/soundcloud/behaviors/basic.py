# -*- coding: utf-8 -*-
from phonogen.site import _
from plone.app.contenttypes.browser.utils import Utils
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as namedfile
from plone.supermodel import model
from Products.Five.browser import BrowserView
from zope import schema
from zope.interface import implementer
from zope.interface import provider
import json


@provider(IFormFieldProvider)
class ISoundCloudBasic(model.Schema):
    """Adds SoundCloud specific fields
    """

    # Preview File for SoundCloud
    asset_data = namedfile.NamedBlobFile(
        title=_(u'label_asset_data',
                u'Soundcloud Player File (WZ)'),
        required=False
    )

    sharing = schema.Choice(
        title=_(u'label_sharing', default=u'Sharing'),
        required=False,
        vocabulary='soundcloud.sharing'
    )

    downloadable = schema.Choice(
        title=_(u'label_downloadable', default=u'Downloads'),
        required=False,
        vocabulary='soundcloud.download'
    )

    trackdata = schema.Text(
        title=_(u'label_trackdata', default=u'Soundcloud Track Data'),
        required=False,
    )


@implementer(ISoundCloudBasic)
class SoundCloudBasic(object):
    """
    """

    def __init__(self, context):
        self.context = context


class SoundCloudBasicView(Utils):

    def __init__(self, context, request):
        super(SoundCloudBasicView, self).__init__(context, request)

    def is_videotype(self):
        ct = self.context.file.contentType
        return 'video/' in ct

    def is_audiotype(self):
        ct = self.context.file.contentType
        return 'audio/' in ct

    def get_mimetype_icon(self):
        return super(SoundCloudBasicView, self).getMimeTypeIcon(self.context.file)

    def track(self):
        return json.loads(self.context.trackdata)
