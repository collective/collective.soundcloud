# -*- coding: utf-8 -*-
from plone.supermodel.directives import MetadataListDirective
from plone.supermodel.utils import mergedTaggedValueList
from plone.behavior.interfaces import IBehaviorAssignable

SOUNDCLOUD_KEY = 'collective.soundcloud.metainfo.fields'
SOUNDFILE_KEY = 'collective.soundcloud.metainfo.file'
ARTWORKFILE_KEY = 'collective.soundcloud.metainfo.file'


class SoundcloudMeta(object):

    def __init__(self, accessors=[], soundfile=None, artworkfile=None):
        self.soundfile = soundfile
        self.artworkfile = artworkfile
        self.accessors = accessors


class soundcloud(MetadataListDirective):
    """Directive used find soudncloud data accessors
    """
    key = SOUNDCLOUD_KEY

    def factory(self, *args):
        metainfo = SoundcloudMeta(accessors=args)
        return [metainfo]


class soundfile(MetadataListDirective):
    """Directive used to create fieldsets
    """
    key = SOUNDFILE_KEY

    def factory(self, filefield):
        metainfo = SoundcloudMeta(soundfile=filefield)
        return [metainfo]


class artworkfile(MetadataListDirective):
    """Directive used to create fieldsets
    """
    key = ARTWORKFILE_KEY

    def factory(self, filefield):
        metainfo = SoundcloudMeta(artworkfile=filefield)
        return [metainfo]


def get_soundfile_field(context):
    assignable = IBehaviorAssignable(context, None)
    if assignable is None:
        return
    for behavior_registration in assignable.enumerateBehaviors():
        schema = behavior_registration.interface
        for tgv in mergedTaggedValueList(schema, SOUNDFILE_KEY):
            if tgv.soundfile:
                return tgv.soundfile


def get_artworkfile_field(context):
    assignable = IBehaviorAssignable(context, None)
    if assignable is None:
        return
    for behavior_registration in assignable.enumerateBehaviors():
        schema = behavior_registration.interface
        for tgv in mergedTaggedValueList(schema, SOUNDFILE_KEY):
            if tgv.soundfile:
                return tgv.soundfile


def get_soundcloud_accessors(context):
    accessors = []
    assignable = IBehaviorAssignable(context, None)
    if assignable is None:
        return accessors
    for behavior_registration in assignable.enumerateBehaviors():
        schema = behavior_registration.interface
        for tgv in mergedTaggedValueList(schema, SOUNDCLOUD_KEY):
            for accessor in tgv.accessors:
                accessors.append((schema, accessor,))
    return accessors
