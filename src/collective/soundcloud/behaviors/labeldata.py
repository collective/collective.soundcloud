# -*- coding: utf-8 -*-
from collective.soundcloud import _
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
class ISoundCloudLabelData(model.Schema):
    """Adds SoundCloud Record Label specific fields
    """

    SOUNDCLOUD_ACCESSORS = [
        'label',
        'release_day',
        'release_month',
        'release_year',
        'downloadable',
        'trackdata',
    ]

    label = schema.TextLine(
        title=_(u'label_label', default=u'Label'),
        required=False,
    )

    release_date = schema.Date(
        title=_(u'label_release_date',
                u'Release Date'),
        required=False
    )

    release_day = Attribute('relase day')
    release_month = Attribute('relase day')
    release_year = Attribute('relase day')

    release = schema.TextLine(
        title=_(u'label_release', default=u'Release/Catalogue Number'),
        required=False,
    )

    isrc = schema.TextLine(
        title=_(u'label_isrc', default=u'ISRC'),
        required=False,
    )

    license = schema.Choice(
        title=_(u'label_license', default=u'License'),
        required=False,
        vocabulary='soundcloud.licences',
        default='all-rights-reserved',
    )

    buy_link = schema.TextLine(
        title=_(u'label_buy_link', default=u'Buy Link'),
        required=False,
    )

    video_link = schema.TextLine(
        title=_(u'label_video_link', default=u'Video Link'),
        required=False,
    )


@implementer(ISoundCloudLabelData)
class SoundCloudLabelData(object):
    """
    """

    def __init__(self, context):
        self.context = context

    @property
    def release_date(self):
        return self.context.release_date

    @property.setter
    def release_date(self, value):
        self.context.release_date = value

    @property
    def release_day(self)
        self.context.release_date.day  # XXX implement me
