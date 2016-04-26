# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from collective.soundcloud.events import SoundcloudCreatedEvent
from collective.soundcloud.events import SoundcloudModifiedEvent
from collective.soundcloud.utils import get_soundcloud_api
from zope.event import notify
from plone.behavior.interfaces import IBehaviorAssignable


class SoundcloudUploaderView(BrowserView):

    def async_upload_handler(self):
        sc = get_soundcloud_api()

        # fetch fields and blob
        assignable = IBehaviorAssignable(self, None)
        if assignable is not None:
            for behavior_registration in assignable.enumerateBehaviors():
                pass

        if self.soundcloud_id:
            # we're are in soundcloud edit mode,
            # iow this was already uploaded to soundcloud
            tracks = sc.tracks(self.soundcloud_id)
            if tfname:
                tracks(delete=True)
                tracks = sc.tracks()
        else:
            # no soundcloud upload so far.
            tracks = sc.tracks()

        assignable = IBehaviorAssignable(self, None)
        if assignable is not None:
            for behavior_registration in assignable.enumerateBehaviors():
                pass

        if tfname:
            tdir = os.path.dirname(tfname)
            try:
                tf = open(tfname, 'rb')
                upload_track_data['asset_data'] = tf
                upload_track_data = upload(tracks, upload_track_data)
            finally:
                tf.close()
                shutil.rmtree(tdir)
        else:
            upload_track_data = upload(tracks, upload_track_data)
        setattr(context, 'trackdata', upload_track_data)
        setattr(context, 'soundcloud_id', upload_track_data['id'])
        self.context._p_changed = 1
        if mode == 'edit':
            notify(SoundcloudModifiedEvent(context))
        else:
            notify(SoundcloudCreatedEvent(context))


    def __call__(self):
        pass
