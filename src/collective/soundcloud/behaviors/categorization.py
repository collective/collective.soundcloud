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
class ISoundCloudCategorization(model.Schema):
    """Adds SoundCloud specific fields
    """

    track_type = schema.Choice(
        title=_(u'label_track_type', default=u'Track Type'),
        required=False,
        vocabulary='soundcloud.tracktypes'
    )

    genre = schema.TextLine(
        title=_(u'label_genre', default=u'Genre'),
        required=False,
    )

    tags = schema.List(
        title=_(u'label_tags', default=u'Tags'),
        required=False,
    )

    bpm = schema.TextLine(
        title=_(u'label_bpm', default=u'BPM'),
        required=False,
    )


@implementer(ISoundCloudCategorization)
class SoundCloudCategorization(object):
    """
    """

    def __init__(self, context):
        self.context = context
