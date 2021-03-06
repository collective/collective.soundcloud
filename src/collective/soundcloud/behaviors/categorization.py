# -*- coding: utf-8 -*-
from collective.soundcloud import _
from collective.soundcloud import directives
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.z3cform.textlines import TextLinesFieldWidget
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


@provider(IFormFieldProvider)
class ISoundCloudCategorization(model.Schema):
    """Adds SoundCloud specific fields
    """

    directives.soundcloud(
        'track_type',
        'genre',
        'bpm',
    )

    track_type = schema.Choice(
        title=_(u'label_track_type', default=u'Track Type'),
        required=False,
        vocabulary='soundcloud.tracktypes'
    )

    genre = schema.TextLine(
        title=_(u'label_genre', default=u'Genre'),
        required=False,
    )

    bpm = schema.Float(
        title=_(u'label_bpm', default=u'BPM'),
        required=False,
    )


class ISoundCloudCategorizationMarker(Interface):
    """ """


@implementer(ISoundCloudCategorization)
class SoundCloudCategorization(object):
    """
    """

    def __init__(self, context):
        self.context = context

    @property
    def track_type(self):
        return self.context.track_type

    @track_type.setter
    def track_type(self, value):
        self.context.track_type = value

    @property
    def genre(self):
        return self.context.genre

    @genre.setter
    def genre(self, value):
        self.context.genre = value

    @property
    def bpm(self):
        return self.context.bpm

    @bpm.setter
    def bpm(self, value):
        self.context.bpm = value
