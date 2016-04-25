# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


class ISoundcloudCreatedEvent(IObjectCreatedEvent):
    """New asset created in soundcloud by Plone"""


class ISoundcloudModifiedEvent(IObjectModifiedEvent):
    """Existing asset modified in soundcloud by Plone"""


@implementer(ISoundcloudCreatedEvent)
class SoundcloudCreatedEvent(ObjectCreatedEvent):
    """ """


@implementer(ISoundcloudModifiedEvent)
class SoundcloudModifiedEvent(ObjectCreatedEvent):
    """ """
