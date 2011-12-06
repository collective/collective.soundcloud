from zope.interface import (
    implementer,
    invariant, 
    Invalid,
)    
from zope.component import adapter
from zope.lifecycleevent.interfaces import (
    IObjectCreatedEvent,
    IObjectModifiedEvent,
)    
from zope import schema
from zope.schema.vocabulary import (
    SimpleVocabulary, 
    SimpleTerm,
)
from zope.i18nmessageid import MessageFactory
from five import grok
from plone.directives import form, dexterity
from collective.soundcloud.utils import (
    get_soundcloud_api,
    player_url,
    validate_user,
    validate_set,
)

_ = MessageFactory("collective.soundcloud")

listing_types = SimpleVocabulary([
     SimpleTerm(value=u'set', title=_(u'Set')),
     SimpleTerm(value=u'user', title=_(u'Tracks of a User')),
])

PLAYER = u"http://api.soundcloud.com/tracks/%s"

class TypeInvariantInvalid(Invalid):
    __doc__ = _(u"If type is user either 'you' or a username must be provided.")

class IListing(form.Schema):
    """A soundcloud set, playlist or me/users tracks.
    """
        
    sc_type = schema.Choice(
            title=_(u"Type of Listing"),
            vocabulary=listing_types,
            required=True,
        )         

    sc_id = schema.TextLine(
            title=_(u"ID or URL"),
            required=False,
        )         
        

    sc_you = schema.Bool(
            title=_(u"You"),
        )         

    sc_filter = schema.TextLine(
            title=_(u"Fulltext-Filter"),
            required=False,
        )         

    sc_filter = schema.TextLine(
            title=_(u"Tags-Filter"),
            required=False,
        )         


    @invariant
    def validate_listing_type(data):
        sc = get_soundcloud_api()        
        if data.sc_type == u'user':
            if data.sc_you or data.sc_id:
                if data.sc_id:
                    code, msg, newid = validate_user(data.sc_id)
                    if code <= 0:
                        return
                    msg = _('The provided users URL or ID is not valid: %s') %\
                          msg
                else: 
                    return
            elif data.sc_you and data.sc_id:
                msg = _('Provide either user URL or ID or *you*, not both.')
            else: 
                msg = _('User listing type requires an User or *you*')
        else:
            if data.sc_id:
                code, msg, newid = validate_set(data.sc_id)
                if code <= 0:
                    return
                msg = _('The provided Set URL or ID is not valid: %s') %\
                      msg
            else:
                msg = _('Set listing type requires a Set URL/ID')
        raise TypeInvariantInvalid(msg)    
           
           
@grok.subscribe(IListing, IObjectCreatedEvent)    
@grok.subscribe(IListing, IObjectModifiedEvent)    
def listing_lookup_handler(listing, event):
    if listing.sc_type == 'user':
        if listing.sc_id:        
            code, msg, newid = validate_user(listing.sc_id)
            if code < 0:
                listing.sc_id = newid
    else: # type == 'set'
        code, msg, newid = validate_set(listing.sc_id)
        if code < 0:            
            listing.sc_id = newid

    
class View(grok.View):
    grok.context(IListing)
    grok.require('zope2.View')
    
    @property
    def is_set(self):
        return self.context.sc_type == 'set'
    
    @property
    def is_user(self):
        return self.context.sc_type == 'user'
    
    def tracks(self):
        """list of dicts, each dict is a track
        """
        tracks = list()
        sc = get_soundcloud_api()
        if self.is_set:
            scset = sc.playlists(self.context.sc_id)
            tracks = scset()['tracks']
        else:
            if self.context.sc_you:
                user = sc.me()
            else:
                user = sc.users(self.context.sc_id)
            tracks = user.tracks()
        for track in tracks:
            track[u'player_url'] = player_url(track['id'])
        return tracks
    
    def pprint(self, track):
        import pprint
        return pprint.pformat(track)        
