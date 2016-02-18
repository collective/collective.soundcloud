from zope.interface import implements
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from collective.soundcloud.interfaces import ISoundcloudSettings


class GlobalSettingsUtility(SimpleItem):

    implements(ISoundcloudSettings)

    security = ClassSecurityInfo()

    def __init__(self, _id='scsettings', title=None):
        super(GlobalSettingsUtility, self).__init__()
        self.id = _id
        self.title = title
        self._client_id = None
        self._client_secret = None
        self._token = None

    security.declareProtected('Manage portal', 'client_id')

    def _get_id(self):
        return self._client_id

    def _set_id(self, value):
        self._client_id = value
    client_id = property(_get_id, _set_id)

    security.declareProtected('Manage portal', 'client_secret')

    def _get_secret(self):
        return self._client_secret

    def _set_secret(self, value):
        self._client_secret = value
    client_secret = property(_get_secret, _set_secret)

    security.declareProtected('Manage portal', 'token')

    def _get_token(self):
        return self._token

    def _set_token(self, value):
        self._token = value
    token = property(_get_token, _set_token)
