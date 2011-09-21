from zope.interface import implementer
from zope.component import adapter
from.zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from zope import schema
from zope.i18nmessageid import MessageFactory
from five import grok
from plone.directives import form, dexterity
from collective.soundcloud.utils import (
    get_soundcloud_api,
    validate_track,
)

_ = MessageFactory("collective.soundcloud")


class ITrack(form.Schema):
    """A soundcloud track.
    """
        
    soundcloud_track = schema.TextLine(
            title=_(u"URL or ID of soundcloud item"),
        )         
       
@grok.subscribe(ITrack, IObjectAddedEvent)    
@grok.subscribe(ITrack, IObjectModifiedEvent)    
def track_lookup_handler(track, event):
    if not track.soundcloud_track.strip():
        return
    code, msg = validate_track(track.soundcloud_track)
    sc = get_soundcloud_api()
    if code < 0:
        trackid = sc.resolve(track.soundcloud_track)
        track.soundcloud_track = trackid
    elif code > 0:
        track.soundcloud_track = '%s (INVALID: %s)' % (track.soundcloud_track,
                                                      msg) 
        return    
    trackdata = sc.tracks(track.soundcloud_track)()
    track.title = trackdata['title']