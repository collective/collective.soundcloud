# -*- coding: utf-8 -*-
from collective.soundcloud.directives import get_soundcloud_accessors
from collective.soundcloud.directives import get_soundfile_field
from collective.soundcloud.events import SoundcloudCreatedEvent
from collective.soundcloud.events import SoundcloudModifiedEvent
from collective.soundcloud.utils import get_soundcloud_api
from Products.Five import BrowserView
from restkit import RequestError
from zope.event import notify

import logging


logger = logging.getLogger(__name__)


class SoundcloudUploaderView(BrowserView):

    def upload(self, tracks, upload_track_data):
        try:
            return tracks(upload_track_data)
        except RequestError:
            logger.exception('Can not modify at/upload to Soundcloud!')
            raise

    def async_upload_handler(self, changed_fields):
        sc = get_soundcloud_api()
        filefield = get_soundfile_field(self.context)
        accessors = get_soundcloud_accessors(self.context)
        import pdb; pdb.set_trace()

        file_has_changed = filefield in changed_fields
        mode = 'edit' if self.context.soundcloud_id else 'add'
        # fetch blob
        if self.context.soundcloud_id:
            # we're are in soundcloud edit mode,
            # iow this was already uploaded to soundcloud
            tracks = sc.tracks(self.soundcloud_id)
            if file_has_changed:
                # delete what we have at soundcloud and create new entry
                tracks(delete=True)
                tracks = sc.tracks()
        else:
            # no soundcloud upload so far.
            tracks = sc.tracks()

        upload_track_data = {}
        for iface, accessor in accessors:
            adapter = iface(self.context)
            upload_track_data[accessor] = getattr(adapter, accessor)

        if file_has_changed:
            # fetch blob as open file-like object
            file_handle = None  # XXX
            upload_track_data['asset_data'] = file_handle
        upload_track_data = self.upload(tracks, upload_track_data)
        setattr(self.context, 'trackdata', upload_track_data)
        setattr(self.context, 'soundcloud_id', upload_track_data['id'])
        self.context._p_changed = 1
        if mode == 'edit':
            notify(SoundcloudModifiedEvent(self.context))
        else:
            notify(SoundcloudCreatedEvent(self.context))

    def __call__(self):
        self.async_upload_handler()
        return 'foo'
