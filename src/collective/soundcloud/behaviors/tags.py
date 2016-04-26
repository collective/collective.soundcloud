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
class ISoundCloudTags(model.Schema):
    """Adds SoundCloud specific tags
    """

    directives.soundcloud(
        'tags',
    )

    widget('tags', TextLinesFieldWidget)
    tags = schema.List(
        title=_(u'label_tags', default=u'Tags'),
        required=False,
        value_type=schema.TextLine(),
    )


class ISoundCloudTagsMarker(Interface):
    """ """


@implementer(ISoundCloudTags)
class SoundCloudTags(object):
    """
    """

    def __init__(self, context):
        self.context = context

    @property
    def tags(self):
        return self.context.tags

    @tags.setter
    def tags(self, value):
        self.context.tags = value
