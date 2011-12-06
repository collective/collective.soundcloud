from zope.interface import (
    Interface,
    Attribute,
)

class SoundcloudLayer(Interface):
    """Browserlayer for soundcloud view, resources, etc."""

class ISoundcloudSettings(Interface):
    
    client_id = Attribute(u'OAuth2 client id, provided by soundcloud.com')
    client_secret = Attribute(u'OAuth2 client secret, provided by '
                              u'soundcloud.com')
    token = Attribute(u'OAuth2 authentication token of an user.')
    
class ISoundcloudItem(Interface):
    """A soundcloud item.
    """        
    soundcloud_id = Attribute(u"URL or ID of soundcloud item")