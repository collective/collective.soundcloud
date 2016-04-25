# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import Attribute
from zope.publisher.interfaces.browser import IBrowserPublisher


class SoundcloudLayer(Interface):
    """Browserlayer for soundcloud view, resources, etc."""


class ISoundcloudItem(Interface):
    """A soundcloud item.
    """
    soundcloud_id = Attribute(u"ID of soundcloud item")

    trackdata = Attribute(
        u'dict with the trackdata fetched from soundcloud api')


class ISoundcloudPublisher(ISoundcloudItem, IBrowserPublisher):
    """Published Soundcloud Item"""
