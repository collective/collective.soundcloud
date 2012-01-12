from zope.interface import implementer
from zope.component import adapter
from zope import schema
from zope.i18nmessageid import MessageFactory
from plone.directives import form, dexterity
from zope.publisher.browser import BrowserView
from collective.soundcloud.utils import (
    get_soundcloud_api,
    player_url,
    validate_track,
)
from collective.soundcloud.interfaces import ISoundcloudItem

_ = MessageFactory("collective.soundcloud")

def alias_validator(value):
    code, msg, newid = validate_track(value)
    if code > 0:
        return False
    if code < 0:
        value = newid
    sc = get_soundcloud_api()
    return code <= 0 and not 'error' in sc.tracks(value)()       


class IAlias(form.Schema, ISoundcloudItem):
    """A soundcloud alias.
    """
        
    soundcloud_id = schema.TextLine(
            title=_(u"URL or ID of soundcloud item"),
            required=True,
            constraint=alias_validator,
        )      
   
def alias_lookup_handler(alias, event):
    sc = get_soundcloud_api()
    
    alias.soundcloud_id = sc.resolve(alias.soundcloud_id)
    alias.trackdata = sc.tracks(alias.soundcloud_id)()    
    
class View(BrowserView):
    
    def url(self):
        return player_url(self.context.soundcloud_id)