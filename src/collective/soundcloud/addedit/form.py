import copy
from zope.i18nmessageid import MessageFactory
from zExceptions import Unauthorized
from Products.Five import BrowserView
import yafowil.zope2
from yafowil.base import UNSET
from yafowil.controller import Controller
from yafowil.yaml import parse_from_YAML
from collective.soundcloud.interfaces import ISoundcloudItem
from collective.soundcloud.utils import get_soundcloud_api

_ = MessageFactory('collective.soundcloud')

EDIT, ADD = 1, 2
DEFAULTS = {
    'title': UNSET,
    'description': UNSET,
    'asset_data': UNSET,
}  

class SoundcloudAddEdit(BrowserView):    
    
    def form(self):
        self.mode = ADD        
        self.trackdata = copy.deepcopy(DEFAULTS)
        if ISoundcloudItem.providedBy(self.context):
            self.mode = EDIT
            self.trackdata = copy.deepcopy(self.context.trackdata)
        form = parse_from_YAML('collective.soundcloud.addedit:form.yaml',
                               self,  _)        
        controller = Controller(form, self.request)
        if not controller.next:
            return controller.rendered        
        self.request.RESPONSE.redirect(controller.next)
            
    def next(self, request):
        if self.mode == ADD:
            return '%s/++soundcloud++%s' % (self.context.absolute_url(), 
                                            self.soundcloud_id)
        else:
            return self.context.absolute_url()

    @property
    def action(self):
        return '%s/@@soundcloud_modifier' % self.context.absolute_url() 
    
    def save(self, widget, data):
        if self.request.method != 'POST':
            raise Unauthorized('POST only')
        # upload here
        upload_track_data = dict()
        upload_track_data['title'] = data['title'].extracted
        upload_track_data['description'] = data['description'].extracted 
        upload_track_data['asset_data'] = data['soundfile'].extracted['file']
        sc = get_soundcloud_api()
        tracks = sc.tracks()        
        trackdata = tracks(upload_track_data)
        if self.mode == EDIT:
            self.context.trackdata = trackdata
        self.soundcloud_id = trackdata
