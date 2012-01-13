from zope.interfaces import implements
from zope.lifecyclevent import (
    ObjectCreatedEvent, 
    ObjectModifiedEvent
)
from zope.lifecyclevent.interfaces import (
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