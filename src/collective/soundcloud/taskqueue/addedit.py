# -*- coding: utf-8 -*-
from collective.taskqueue.taskqueue import add

import hashlib


def _queue_upload(obj, asset_changed=True):
    """if descriptions is None, this is an add
    """
    url = '/'.join(obj.getPhysicalPath()) + '/@@soundcloud_uploader'
    add(url, params={'asset_changed': asset_changed}, payload=None)


def md5(blob):
    hash_md5 = hashlib.md5()
    with blob.open() as fd:
        for chunk in iter(lambda: fd.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_hash(obj):
    return getattr(obj, '_asset_data_hash', None)


def set_hash(obj):
    blob = getattr(obj, 'asset_data', None)
    if blob:
        obj._asset_data_hash = md5(blob)
    return get_hash(obj)


def soundcloud_add(obj, event):
    set_hash(obj)
    _queue_upload(obj)


def soundcloud_modified(obj, event):
    old_hash = get_hash(obj)
    new_hash = set_hash(obj)
    _queue_upload(obj, asset_changed=old_hash != new_hash)
