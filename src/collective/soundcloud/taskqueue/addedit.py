# -*- coding: utf-8 -*-


def queue_upload(obj, descriptions=None):
    """if descriptions is None, this is an add
    """

    if descriptions is None:
        # add, all fields are changed
        pass
    else:
        if len(descriptions) == 0:
            return
        # edit, look which relevant fields are changed
        pass


def soundcloud_add(obj, event):
    queue_upload(obj, mode='add')


def soundcloud_edit(obj, event):
    queue_upload(obj, event.descriptions=[])
