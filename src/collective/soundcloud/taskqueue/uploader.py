# -*- coding: utf-8 -*-
from collective.soundcloud.directives import get_soundcloud_accessors
from collective.soundcloud.directives import get_soundfile_field
from collective.soundcloud.events import SoundcloudCreatedEvent
from collective.soundcloud.events import SoundcloudModifiedEvent
from collective.soundcloud.utils import get_soundcloud_api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
#from restkit import RequestError
from StringIO import StringIO
from zope.event import notify
from zope.interface import alsoProvides

import logging


logger = logging.getLogger(__name__)


class SoundcloudUploaderView(BrowserView):

    def upload(self, tracks, upload_track_data):
        try:
            return tracks(upload_track_data)
        except Exception as e:
            import ipdb; ipdb.set_trace()
            logger.exception('Can not modify at/upload to Soundcloud!')
            raise

    def _prepare_upload_data(self, filefield, asset_data_changed):
        track_data = {}
        accessors = get_soundcloud_accessors(self.context)
        for iface, accessor in accessors:
            if accessor == 'asset_data' and not asset_data_changed:
                continue
            adapter = iface(self.context)
            value = getattr(adapter, accessor)
            if value is None:
                continue
            track_data[accessor] = value
            if accessor == filefield:
                # pass an open blob in
                track_data[accessor] = StringIO(track_data[accessor].data)
                track_data[accessor].name = self.context.getId()
                continue

            if isinstance(track_data[accessor], unicode):
                track_data[accessor] = track_data[accessor].encode('utf-8')
            elif isinstance(track_data[accessor], list):
                track_data[accessor] = ' '.join(
                    [
                        '"{0}"'.format(
                            _.encode('utf-8').strip().replace('"', '\\"')
                        )
                        for _ in track_data[accessor]
                    ]
                )
            elif not isinstance(track_data[accessor], basestring):
                track_data[accessor] = str(track_data[accessor])
        return track_data

    def _notify(self, mode):
        if mode == 'edit':
            notify(SoundcloudModifiedEvent(self.context))
        else:
            notify(SoundcloudCreatedEvent(self.context))

    def _tracks(self, filefield, asset_data_changed, mode):
        sc = get_soundcloud_api()
        if mode == 'edit':
            # this was already uploaded to soundcloud
            tracks = sc.tracks(self.context.soundcloud_id)
            if asset_data_changed:
                # delete what we have at soundcloud and create new entry
                try:
                    tracks(delete=True)
                except:
                    pass
                # create a new one
                tracks = sc.tracks()
            return tracks
        # no soundcloud upload so far, using this a new entry will be created
        return sc.tracks()

    def _save(self, track_data):
        setattr(self.context, 'trackdata', track_data)
        setattr(self.context, 'soundcloud_id', track_data['id'])
        self.context._p_changed = 1

    def __call__(self):
        self.request._sc_upload = True
        alsoProvides(self.request, IDisableCSRFProtection)

        self.request.response.setHeader('Content-Type', 'application/json')
        asset_data_changed = self.request.form.get('asset_changed', 'False')
        asset_data_changed = asset_data_changed == 'True'

        filefield = get_soundfile_field(self.context)
        upload_data = self._prepare_upload_data(filefield, asset_data_changed)
        if not upload_data:
            return
        mode = 'edit' if self.context.soundcloud_id else 'add'
        sc_tracks = self._tracks(filefield, asset_data_changed, mode)
        track_data = self.upload(sc_tracks, upload_data)
        self._save(track_data)
        self._notify(mode)
        return ''
