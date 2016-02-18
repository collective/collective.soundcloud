from zope.interface import implements
from zope.lifecycleevent import (
    ObjectCreatedEvent,
    ObjectModifiedEvent
)
from zope.lifecycleevent.interfaces import (
    IObjectCreatedEvent,
    IObjectModifiedEvent
)


class ISoundcloudCreatedEvent(IObjectCreatedEvent):
    """New asset created in soundcloud by Plone"""


class ISoundcloudModifiedEvent(IObjectModifiedEvent):
    """Existing asset modified in soundcloud by Plone"""


class SoundcloudCreatedEvent(ObjectCreatedEvent):
    implements(ISoundcloudCreatedEvent)


class SoundcloudModifiedEvent(ObjectCreatedEvent):
    implements(ISoundcloudModifiedEvent)
