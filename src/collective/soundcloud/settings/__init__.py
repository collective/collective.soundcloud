from zope.component import getUtility
from collective.soundcloud.interfaces import ISoundcloudSettings


def get_soundcloud_settings():
    return getUtility(ISoundcloudSettings)
