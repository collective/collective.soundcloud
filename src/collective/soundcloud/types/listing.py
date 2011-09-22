from zope.interface import (
    implementer,
    invariant, 
    Invalid,
)    
from zope.component import adapter
from.zope.lifecycleevent.interfaces import (
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
    validate_track,
)

_ = MessageFactory("collective.soundcloud")

listing_types = SimpleVocabulary([
     SimpleTerm(value=u'set', title=_(u'Set')),
     SimpleTerm(value=u'user', title=_(u'Tracks of a User')),
])

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
            title=_(u"Set ID or URL"),
            required=False,
        )         

    sc_user = schema.TextLine(
            title=_(u"User ID or URL"),
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
        if data.sc_type == u'user':
            if data.sc_you or data.sc_user:
                if data.sc_user:
                    # XXX validate userid
                    # msg = _('The provided users name or id is not valid')
                    return            
                else: 
                    return
            elif data.sc_you and data.sc_user:
                msg = _('Provide either user or *you*, not both.')
            else: 
                msg = _('Selected listing type requires an user or *you*')
        else:
            if data.sc_id:
                # XXX validate set id
                return
            msg = _('Selected listing type requires an URL/ID')
        raise TypeInvariantInvalid(msg)    
           
           
@grok.subscribe(IListing, IObjectCreatedEvent)    
@grok.subscribe(IListing, IObjectModifiedEvent)    
def track_lookup_handler(listing, event):
    if not hasattr(listing, 'title'):
        listing.title = ''
    if not hasattr(listing, 'description'):
        listing.description = ''
    return # XXX
    
#class View(grok.View):
#    grok.context(IListing)
#    grok.require('zope2.View')