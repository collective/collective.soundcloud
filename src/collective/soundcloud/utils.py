import re
from collective.soundcloud.settings import get_soundcloud_settings
from soundcloudapi import (
    AuthInfo, 
    Soundcloud,
    SoundcloudException,
) 

SC_URLMATCH1 = re.compile(r'https?://soundcloud.com/\S+?/\S+?$')
SC_URLMATCH2 = re.compile(r'https?://soundcloud.com/\S+?/\S+?/{1}?.*$')

def get_soundcloud_api():
    se = get_soundcloud_settings()
    ai = AuthInfo(se.client_id, client_secret=se.client_secret, token=se.token)
    return Soundcloud(ai)

def validate_track(trackid):
    try:
        # pre-flight - check if valid int
        int(trackid)
    except ValueError:
        if SC_URLMATCH1.match(trackid) and not SC_URLMATCH2.match(trackid):
            return -1, 'Track looks like an URL to an track'
        return 1, 'Track Id is not an integer.' 
    # flight: api
    sc = get_soundcloud_api()
    try:
        track = sc.tracks(trackid)()
        # XXX error in track?
    except SoundcloudException:        
        return 2, 'Track Id is not valid according to soundcloud.com.'
    return 0, 'OK'