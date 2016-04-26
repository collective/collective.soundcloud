# -*- coding: utf-8 -*-
from collective.soundcloud import _
from collective.soundcloud import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.interface import provider
from zope.interface import Attribute


@provider(IFormFieldProvider)
class ISoundCloudLabelData(model.Schema):
    """Adds SoundCloud Record Label specific fields
    """

    directives.soundcloud(
        'label',
        'release_day',
        'release_month',
        'release_year',
        'isrc',
        'license',
        'buy_link',
        'video_link',
    )

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
    def label(self):
        return self.context.label

    @label.setter
    def label(self, value):
        self.context.label = value

    @property
    def release_date(self):
        return self.context.release_date

    @release_date.setter
    def release_date(self, value):
        self.context.release_date = value

    @property
    def release_day(self):
        if not self.context.release_date:
            return "None"
        return self.context.release_date.day

    @property
    def release_month(self):
        if not self.context.release_date:
            return "None"
        return self.context.release_date.month

    @property
    def release_year(self):
        if not self.context.release_date:
            return "None"
        return self.context.release_date.year

    @property
    def isrc(self):
        return self.context.isrc

    @isrc.setter
    def isrc(self, value):
        self.context.isrc = value

    @property
    def license(self):
        return self.context.license

    @license.setter
    def license(self, value):
        self.context.license = value

    @property
    def buy_link(self):
        return self.context.buy_link

    @buy_link.setter
    def buy_link(self, value):
        self.context.buy_link = value

    @property
    def video_link(self):
        return self.context.video_link

    @video_link.setter
    def video_link(self, value):
        self.context.video_link = value
