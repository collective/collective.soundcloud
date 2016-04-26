# -*- coding: utf-8 -*-
from collective.soundcloud import _
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as namedfile
from plone.supermodel import model
from Products.Five.browser import SoundCloudBasicView
from zope import schema
from zope.interface import implementer
from zope.interface import provider
import json


@provider(IFormFieldProvider)
class ISoundCloudBasic(model.Schema):
    """Adds SoundCloud specific fields
    """

    SOUNDCLOUD_ACCESSORS = [
        'asset_data',
        'sharing',
        'downloadable',
        'trackdata',
    ]

    # Preview File for SoundCloud
    asset_data = namedfile.NamedBlobFile(
        title=_(u'label_asset_data',
                u'Soundcloud Player File (WZ)'),
        required=False
    )

    sharing = schema.Choice(
        title=_(u'label_sharing', default=u'Sharing'),
        required=False,
        vocabulary='phonogen.protraxx.sharing'
    )

    downloadable = schema.Choice(
        title=_(u'label_downloadable', default=u'Downloads'),
        required=False,
        vocabulary='phonogen.protraxx.download'
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

    @property
    def asset_data(self):
        return self.context.asset_data

    @asset_data.setter
    def asset_data(self, value):
        self.context.asset_data = value
