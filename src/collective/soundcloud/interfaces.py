from zope.interface import (
    Interface,
    Attribute,
)

class ISoundcloudSettings(Interface):
    
    client_id = Attribute(u'OAuth2 client id, provided by soundcloud.com')
    client_secret = Attribute(u'OAuth2 client secret, provided by '
                              u'soundcloud.com')
    token = Attribute(u'OAuth2 authentication token of an user.')