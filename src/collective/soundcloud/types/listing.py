from zope.interface import (
    implementer,
    invariant,
    Invalid,
)
from zope.component import adapter
from zope import schema
from zope.schema.vocabulary import (
    SimpleVocabulary,
    SimpleTerm,
)
from zope.publisher.browser import BrowserView
from zope.i18nmessageid import MessageFactory
from plone.autoform import directives as form
from plone.supermodel import model
from collective.soundcloud.utils import (
    get_soundcloud_api,
    player_url,
    validate_user,
    validate_set,
)
import operator

_ = MessageFactory("collective.soundcloud")

listing_types = SimpleVocabulary([
     SimpleTerm(value=u'set', title=_(u'Set')),
     SimpleTerm(value=u'user', title=_(u'Tracks of a User')),
])

sort_order = SimpleVocabulary([
     SimpleTerm(value=u'title', title=_(u'Title')),
     SimpleTerm(value=u'created_at', title=_(u'Date')),
     SimpleTerm(value=u'duration', title=_(u'Duration')),
     SimpleTerm(value=u'shared_to_count', title=_(u'Shared to count')),
     SimpleTerm(value=u'release', title=_(u'Release number')),
     SimpleTerm(value=u'bpm', title=_(u'BPM')),
])

PLAYER = u"http://api.soundcloud.com/tracks/%s"


class TypeInvariantInvalid(Invalid):
    __doc__ = _(u"If type is user either 'you' or a username must be provided.")


class IListing(model.Schema):
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
            title=_(u"Tags-Filter"),
            required=False,
        )

    sc_quantity = schema.Int(
            title=_(u"Number of items"),
            required=False,
        )
    sc_sortorder = schema.Choice(
            title=_(u"Sort Order"),
            required=False,
            vocabulary=sort_order,
        )
    sc_sortreverse = schema.Bool(
            title=_(u"Reverse Order"),
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


def listing_lookup_handler(listing, event):
    if listing.sc_type == 'user':
        if listing.sc_id:
            code, msg, newid = validate_user(listing.sc_id)
            if code < 0:
                listing.sc_id = newid
    else:  # type == 'set'
        code, msg, newid = validate_set(listing.sc_id)
        if code < 0:
            listing.sc_id = newid


class View(BrowserView):

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
            filter = {}
            if self.context.sc_filter:
                filter['tags'] = self.context.sc_filter
            tracks = user.tracks(filter=filter)
        if self.context.sc_sortorder:
            if self.context.sc_sortorder:
                def keygetter(track):
                    return track[self.context.sc_sortorder]
                tracks = sorted(tracks, key=keygetter,
                                reverse=self.context.sc_sortreverse)
        if self.context.sc_quantity:
            tracks = tracks[:self.context.sc_quantity]
        for track in tracks:
            track[u'player_url'] = player_url(track['id'])
        return tracks

    def pprint(self, track):
        import pprint
        return pprint.pformat(track)
