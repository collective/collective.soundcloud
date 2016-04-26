# -*- coding: utf-8 -*-
from collective.soundcloud import _
from collective.soundcloud import directives
from plone.autoform.directives import omitted
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


@provider(IFormFieldProvider)
class ISoundCloudBasic(model.Schema):
    """Adds SoundCloud specific fields
    """

    directives.soundcloud(
        'asset_data',
        'sharing',
        'downloadable',
    )
    directives.soundfile('asset_data')

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

    omitted('trackdata')
    trackdata = schema.Text(
        title=_(u'label_trackdata', default=u'Soundcloud Track Data'),
        required=False,
    )

    omitted('soundcloud_id')
    soundcloud_id = schema.Text(
        title=_(u'label_soundcloud_id', default=u'Soundcloud ID'),
        required=False,
    )


class ISoundCloudBasicMarker(Interface):
    """ """


@implementer(ISoundCloudBasic)
class SoundCloudBasic(object):
    """Adapter for Soundcloud Basics
    """

    def __init__(self, context):
        self.context = context

    @property
    def asset_data(self):
        return self.context.asset_data

    @asset_data.setter
    def asset_data(self, value):
        self.context.asset_data = value

    @property
    def sharing(self):
        return self.context.sharing

    @sharing.setter
    def sharing(self, value):
        self.context.sharing = value

    @property
    def downloadable(self):
        return self.context.downloadable

    @downloadable.setter
    def downloadable(self, value):
        self.context.downloadable = value
