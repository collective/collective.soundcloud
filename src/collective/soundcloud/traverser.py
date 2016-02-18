import time
from zope.interface import implements
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces import (
    NotFound,
    TraversalException,
)
from Acquisition import Implicit, aq_parent, aq_inner
from OFS.SimpleItem import Item
from soundcloudapi import SoundcloudException
from collective.soundcloud.interfaces import ISoundcloudPublisher
from collective.soundcloud.utils import get_soundcloud_api
from plone.memoize import ram


def _cachekey_fetch_track(method, self):
    # TODO: make the caching timeout configurable
    return (self.soundcloud_id, time.time() // 300)


class TrackItem(Implicit, Item):

    implements(ISoundcloudPublisher)

    def __init__(self, scid):
        if not scid:
            raise TraversalException()
        self.soundcloud_id = scid
        self.trackdata = self.fetch_track()

    def browserDefault(self, request):
        return self, ('@@view',)

    @ram.cache(_cachekey_fetch_track)
    def fetch_track(self):
        sc = get_soundcloud_api()
        try:
            trackdata = sc.tracks(self.soundcloud_id)()
        except SoundcloudException as e:
            raise NotFound(self.context, 'no soundcloud track with id: "%s"' %
                           self.soundcloud_id)
        return trackdata

    def getPhysicalPath(self):
        parent = aq_parent(aq_inner(self))
        trav = '++soundcloud++%s' % self.soundcloud_id
        if not hasattr(parent, 'getPhysicalPath'):
            return ('', trav)
        return tuple(list(parent.getPhysicalPath()) + [trav])


class TrackTraverser(object):

    implements(ITraversable)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, scid, subpath):
        return TrackItem(scid).__of__(self.context)
