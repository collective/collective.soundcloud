# -*- coding: utf-8 -*-
from collective.soundcloud.directives import get_soundcloud_accessors
from collective.soundcloud.directives import get_soundfile_field
from collective.soundcloud.events import SoundcloudCreatedEvent
from collective.soundcloud.events import SoundcloudModifiedEvent
from collective.soundcloud.utils import get_soundcloud_api
from Products.Five import BrowserView
from restkit import RequestError
from StringIO import StringIO
from zope.event import notify
from Products.CMFPlone.utils import safe_unicode

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
        file_has_changed = changed_fields and filefield in changed_fields
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
        track_data = {}
        for iface, accessor in accessors:
            if changed_fields and accessor not in changed_fields:
                continue
            adapter = iface(self.context)
            track_data[accessor] = getattr(adapter, accessor)
            if accessor == filefield:
                # pass an open blob in
                track_data[accessor] = StringIO(track_data[accessor].data)
                track_data[accessor].name = self.context.getId()
            elif isinstance(track_data[accessor], unicode):
                track_data[accessor] = track_data[accessor].encode('utf-8')
            elif isinstance(track_data[accessor], list):
                track_data[accessor] =  ' '.join(
                    ['"{0}"'.format(_.encode('utf-8').strip().replace('"', '\\"'))
                    for _ in track_data[accessor]]
                )
            elif not isinstance(track_data[accessor], basestring):
                track_data[accessor] = str(track_data[accessor])
        if not track_data:
            return
        track_data = self.upload(tracks, track_data)
        setattr(self.context, 'trackdata', track_data)
        setattr(self.context, 'soundcloud_id', track_data['id'])
        self.context._p_changed = 1
        if mode == 'edit':
            notify(SoundcloudModifiedEvent(self.context))
        else:
            notify(SoundcloudCreatedEvent(self.context))
        return track_data

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        return self.async_upload_handler([])
