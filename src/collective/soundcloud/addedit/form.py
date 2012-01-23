import copy
from restkit import RequestError
from zope.event import notify
from zope.i18nmessageid import MessageFactory
from zExceptions import Unauthorized
from Products.Five import BrowserView
import yafowil.zope2
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

class SoundcloudAddEdit(BrowserView):    
    
    def _fetch_form(self):
        return parse_from_YAML('collective.soundcloud.addedit:form.yaml',
                               self,  _)
    
    def form(self):
        self.mode = ADD        
        self.trackdata = dict(DEFAULTS)
        self.soundcloud_id = None
        if ISoundcloudItem.providedBy(self.context):
            self.mode = EDIT
            self.trackdata = copy.deepcopy(self.context.trackdata)
            self.trackdata['asset_data'] = FILEMARKER
            self.soundcloud_id = self.trackdata['id']
        form = self._fetch_form() 
        controller = Controller(form, self.request)
        if not controller.next:
            return controller.rendered        
        if "location" not in self.request.RESPONSE.headers:
            self.request.RESPONSE.redirect(controller.next)
            
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
                if data[key].extracted is FILEMARKER:
                    continue
                else:
                    upload_track_data[key] = data[key].extracted['file']
            else:
                upload_track_data[key] = data[key].extracted
            if isinstance(upload_track_data[key], int):
                upload_track_data[key] = str(upload_track_data[key])
            if isinstance(upload_track_data[key], float):
                upload_track_data[key] = '%1.1f' % upload_track_data[key]
        sc = get_soundcloud_api()
        if self.mode == EDIT:
            tracks = sc.tracks(self.context.trackdata['id']) 
        else:
            tracks = sc.tracks()     
        try:
            upload_track_data = tracks(upload_track_data)
        except RequestError:
            # TODO Error handling
            raise
        return upload_track_data
    
    def save(self, widget, data):
        if self.request.method != 'POST':
            raise Unauthorized('POST only')
        trackdata = self._prepare_trackdata(widget, data)
        self.trackdata = trackdata
        self.soundcloud_id = trackdata['id']
        if self.mode == EDIT:
            self.context.trackdata = trackdata
            self.context.soundcloud_id = trackdata['id']
            notify(SoundcloudModifiedEvent(self.context))
        else:
            if ISoundcloudItem.providedBy(self.context):
                setattr(self.context, 'trackdata', trackdata)
                setattr(self.context, 'soundcloud_id', trackdata['id'])
                self.soundcloud_id = trackdata['id']                
            else:
                self.context = TrackItem(trackdata['id']).__of__(self.context)
            notify(SoundcloudCreatedEvent(self.context))

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
    