import os
import copy
import tempfile
import shutil
from restkit import RequestError
from zope.event import notify
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zExceptions import Unauthorized
from plone.app.async.interfaces import IAsyncService
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import yafowil.loader
from yafowil.base import UNSET
from yafowil.controller import Controller
from yafowil.yaml import parse_from_YAML
from collective.soundcloud.interfaces import ISoundcloudItem
from collective.soundcloud.utils import get_soundcloud_api
from collective.soundcloud.traverser import TrackItem
from collective.soundcloud.events import (
    SoundcloudCreatedEvent,
    SoundcloudModifiedEvent
)

_ = MessageFactory('collective.soundcloud')

EDIT, ADD = 1, 2
FILEMARKER = object()
DEFAULTS = {
    'title': UNSET,
    'description': UNSET,
    'asset_data': UNSET,
    'track_type': UNSET,
    'genre': UNSET,
    'tag_list': "",
    'license': 'all-rights-reserved',
    'label_name': UNSET,
    'release_year': UNSET,
    'release_month': UNSET,
    'release_day': UNSET,
    'release': UNSET,
    'isrc': UNSET,
    'bpm': UNSET,
    'key_signature': UNSET,
    'purchase_url': UNSET,
    'video_url': UNSET,
    'sharing': UNSET,
    'downloadable': UNSET,
}

VOCAB_TRACK_TYPES = [
    "",
    "original",
    "remix",
    "live",
    "recording",
    "spoken",
    "podcast",
    "demo",
    "in progress",
    "stem",
    "loop",
    "sound effect",
    "sample",
    "other",
]

VOCAB_LICENSES = [
    "no-rights-reserved",
    "all-rights-reserved",
    "cc-by",
    "cc-by-nc",
    "cc-by-nd",
    "cc-by-sa",
    "cc-by-nc-nd",
    "cc-by-nc-sa",
]

VOCAB_FILEOPTS = [
    ('keep', u'Keep Existing file'),
    ('replace', u'Replace existing file'),
]
VOCAB_SHARING = [
    ('public', u'Public - Makes this track  available to everyone'),
    ('private', u'Private - Only you have access'),
]
VOCAB_DOWNLOAD = [
    ('true', u'Enabled'),
    ('false', u'Disabled'),
]


def upload(tracks, upload_track_data):
    try:
        return tracks(upload_track_data)
    except RequestError:
        # TODO Error handling
        raise


def async_upload_handler(context, upload_track_data, mode, scid):
    sc = get_soundcloud_api()
    tfname = upload_track_data.get('asset_data', None)
    tracks = sc.tracks()
    if mode == EDIT:
        tracks = sc.tracks(scid)
        if tfname:
            tracks(delete=True)
            tracks = sc.tracks()
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
    context._p_changed = 1
    if mode == 'edit':
        notify(SoundcloudModifiedEvent(context))
    else:
        notify(SoundcloudCreatedEvent(context))


class SoundcloudAddEdit(BrowserView):

    template = ViewPageTemplateFile('form.pt')

    def _fetch_form(self):
        return parse_from_YAML('collective.soundcloud.addedit:form.yaml',
                               self, _)

    def __call__(self):
        self.mode = ADD
        self.trackdata = dict(DEFAULTS)
        self.soundcloud_id = None
        if ISoundcloudItem.providedBy(self.context):
            self.mode = EDIT
            self.trackdata = copy.deepcopy(self.context.trackdata)
            self.trackdata['asset_data'] = {}
            self.soundcloud_id = self.trackdata['id']
        form = self._fetch_form()
        self.controller = Controller(form, self.request)

        if not self.controller.next:
            return self.template()
        if "location" not in self.request.RESPONSE.headers:
            self.request.RESPONSE.redirect(self.controller.next)

    def next(self, request):
        return self.context.absolute_url() + '/view'

    @property
    def action(self):
        postfix = self.mode == ADD and 'add' or 'edit'
        url = self.context.absolute_url()
        return '%s/@@soundcloud_%s' % (url, postfix)

    def _prepare_trackdata(self, widget, data):
        upload_track_data = dict()
        for key in DEFAULTS:
            if data[key].extracted is UNSET:
                continue
            if key == 'asset_data':
                if data[key].extracted['action'] == 'keep':
                    continue
                # TODO! fix this.
                # works not over zeos distributed over more than one server
                tdir = tempfile.mkdtemp()
                tfname = os.path.join(tdir, data[key].extracted['filename'])
                with open(tfname, 'wb') as tf:
                    tf.write(data[key].extracted['original'].read())
                upload_track_data[key] = tfname
            else:
                upload_track_data[key] = data[key].extracted
            if isinstance(upload_track_data[key], int):
                upload_track_data[key] = str(upload_track_data[key])
            elif isinstance(upload_track_data[key], float):
                upload_track_data[key] = '%1.1f' % upload_track_data[key]
        return upload_track_data

    def save(self, widget, data):
        if self.request.method != 'POST':
            raise Unauthorized('POST only')
        upload_track_data = self._prepare_trackdata(widget, data)
        async = getUtility(IAsyncService)
        async.queueJob(async_upload_handler, self.context, upload_track_data,
                       self.mode, self.soundcloud_id)
        self.request.response.redirect(self.context.absolute_url() + '/view')

    @property
    def vocab_track_types(self):
        return VOCAB_TRACK_TYPES

    @property
    def vocab_licenses(self):
        return VOCAB_LICENSES

    @property
    def vocab_fileopts(self):
        return VOCAB_FILEOPTS

    @property
    def vocab_sharing(self):
        return VOCAB_SHARING

    @property
    def vocab_download(self):
        return VOCAB_DOWNLOAD
