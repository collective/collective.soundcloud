from zope.i18nmessageid import MessageFactory
from zExceptions import Unauthorized
from Products.Five import BrowserView
import yafowil.zope2
from yafowil.base import UNSET
from yafowil.controller import Controller
from yafowil.yaml import parse_from_YAML

_ = MessageFactory('collective.soundcloud')

class SoundcloudAddEdit(BrowserView):    
    
    def form(self):
        form = parse_from_YAML('collective.soundcloud.add:form.yaml',
                               self,  _)
        controller = Controller(form, self.request)
        if not controller.next:
            return controller.rendered        
        self.request.RESPONSE.redirect(self.action)
            
    def next(self, request):
        # todo
        return 

    @property
    def action(self):
        # todo
        return 
    
    def save(self, widget, data):
        if self.request.method != 'POST':
            raise Unauthorized('POST only')
        # upload here     