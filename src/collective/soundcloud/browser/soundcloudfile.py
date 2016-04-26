from plone.app.contenttypes.browser.utils import Utils




class SoundCloudBasicView(Utils):

    def __init__(self, context, request):
        super(SoundCloudBasicView, self).__init__(context, request)

    def is_videotype(self):
        ct = self.context.file.contentType
        return 'video/' in ct

    def is_audiotype(self):
        ct = self.context.file.contentType
        return 'audio/' in ct

    def get_mimetype_icon(self):
        return super(ProTraxxFileView, self).getMimeTypeIcon(self.context.file)

    def track(self):
        return json.loads(self.context.trackdata)
