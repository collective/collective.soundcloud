from zope.interface import implementer
from zope.component import adapter
from zope.lifecycleevent.interfaces import (
    IObjectCreatedEvent,
    IObjectModifiedEvent,
)    
from zope import schema
from zope.i18nmessageid import MessageFactory
from five import grok
from plone.directives import form, dexterity
from collective.soundcloud.utils import (
    get_soundcloud_api,
    player_url,
    validate_track,
)

_ = MessageFactory("collective.soundcloud")


def track_validator(value):
    code, msg, newid = validate_track(value)
    if code > 0:
        return False
    if code < 0:
        value = newid
    sc = get_soundcloud_api()
    return code <= 0 and not 'error' in sc.tracks(value)()


class ITrack(form.Schema):
    """A soundcloud track.
    """
        
    soundcloud_track = schema.TextLine(
            title=_(u"URL or ID of soundcloud item"),
            required=True,
            constraint=track_validator,
        )         

       
@grok.subscribe(ITrack, IObjectCreatedEvent)    
@grok.subscribe(ITrack, IObjectModifiedEvent)    
def track_lookup_handler(track, event):
    sc = get_soundcloud_api()
    
    track.soundcloud_track = sc.resolve(track.soundcloud_track)
    trackdata = sc.tracks(track.soundcloud_track)()
    track.title = trackdata['title']
    track.description = trackdata['description']
    
class View(grok.View):
    grok.context(ITrack)
    grok.require('zope2.View')
    
    def url(self):
        return player_url(self.context.soundcloud_track)