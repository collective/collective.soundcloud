# -*- coding: utf-8 -*-
from collective.soundcloud.directives import get_soundcloud_accessors
from collective.soundcloud.directives import get_soundfile_field
from collective.soundcloud.events import SoundcloudCreatedEvent
from collective.soundcloud.events import SoundcloudModifiedEvent
from collective.soundcloud.settings import get_soundcloud_settings
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from StringIO import StringIO
from zope.event import notify
from zope.interface import alsoProvides

import logging
import requests
import soundcloud
import json


logger = logging.getLogger(__name__)


class SoundcloudUploaderView(BrowserView):

    def _prepare_upload_data(self, filefield):
        track_data = {}
        accessors = get_soundcloud_accessors(self.context)
        for iface, accessor in accessors:
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

    def _save(self, track_data):
        setattr(
            self.context,
            'trackdata',
            json.dumps(dict(track_data), sort_keys=True, indent=4)
        )
        setattr(self.context, 'soundcloud_id', track_data['id'])
        self.context._p_changed = 1

    def _upload(self, client, upload_track_data, mode):
        track = client.post(
            '/tracks',
            track=upload_track_data
        )
        return track

    def _remove_if_exists(self, client, upload_track_data):
        scid = getattr(self.context, 'soundcloud_id')
        if not scid:
            return
        try:
            client.delete(
                '/tracks/{0}'.format(scid),
            )
        except requests.HTTPError:
            # ignore - looks like scid does not exists
            return

    def __call__(self):
        self.request._sc_upload = True
        alsoProvides(self.request, IDisableCSRFProtection)
        self.request.response.setHeader('Content-Type', 'application/json')

        filefield = get_soundfile_field(self.context)
        upload_data = self._prepare_upload_data(filefield)
        if not upload_data:
            return
        mode = 'edit' if self.context.soundcloud_id else 'add'
        settings = get_soundcloud_settings()
        client = soundcloud.Client(
            client_id=settings.client_id,
            access_token=settings.token
        )
        if mode == 'edit':
            self._remove_if_exists(client, upload_data)
        resource = self._upload(client, upload_data, mode)
        self._save(resource.obj)
        self._notify(mode)
        return ''
