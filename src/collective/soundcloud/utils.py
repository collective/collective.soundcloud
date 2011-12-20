import re
from collective.soundcloud.settings import get_soundcloud_settings
from soundcloudapi import (
    AuthInfo, 
    Soundcloud,
    SoundcloudException,
)

URL_1_OR_MORE = re.compile(r'https?://soundcloud.com/\S+?$')
URL_2_OR_MORE = re.compile(r'https?://soundcloud.com/\S+?/\S+?$')
URL_3_OR_MORE = re.compile(r'https?://soundcloud.com/\S+?/\S+?/\S+?$')
URL_MORE_THAN_2 = re.compile(r'https?://soundcloud.com/\S+?/\S+?/{1}?.*$')
URL_MORE_THAN_3 = re.compile(r'https?://soundcloud.com/\S+?/\S+?/\S+?/{1}?.*$')

def get_soundcloud_api():
    se = get_soundcloud_settings()
    ai = AuthInfo(se.client_id, client_secret=se.client_secret, token=se.token)
    return Soundcloud(ai)

def player_url(trackid):
    url = 'http://player.soundcloud.com/player.swf?'  
    url += "url=http://api.soundcloud.com/tracks/%s" % trackid
    return url


def _validate_url_or_id(scid, name, match, notmatch, fetcher):
    try:
        int(scid)
    except TypeError:
        return 1, 'Input type given is not valid.'
    except ValueError:
        scid = scid.strip('/')
        if match.match(scid) and not notmatch.match(scid):
            sc = get_soundcloud_api()
            resolvedid = sc.resolve(scid)
            if resolvedid:
                # if resolved we believe soundcloud its existence
                return -1, '%s Id looks like an URL' % name, resolvedid
            return 1, 'Can not resolve %s URL' % name, None
        return 1, '%s Id is not an integer nor an valid URL.' % name, None 
    try:
        fetcher(scid)
        # XXX check error in fetched result?
    except SoundcloudException:        
        return 1, '%s Id is not valid according to soundcloud.com.' % name, None
    return 0, 'OK', None        


def validate_user(userid):
    sc = get_soundcloud_api()    
    return _validate_url_or_id(userid, 'User', 
                               URL_1_OR_MORE, URL_2_OR_MORE,
                               sc.users)

def validate_track(trackid):
    sc = get_soundcloud_api()    
    # XXX buggy, finally we need tests
    return _validate_url_or_id(trackid, 'Track', 
                               URL_2_OR_MORE, URL_MORE_THAN_2,
                               sc.tracks)
    
def validate_set(setid):
    sc = get_soundcloud_api()    
    return _validate_url_or_id(setid, 'Set', 
                               URL_3_OR_MORE, URL_MORE_THAN_3,
                               sc.playlists)    