# -*- coding: utf-8 -*-
from plone.supermodel.directives import MetadataListDirective

SOUNDCLOUD_KEY = 'collective.soundcloud.metainfo.fields'
SOUNDFILE_KEY = 'collective.soundcloud.metainfo.file'


class SoundcloudMeta(object):

    def __init__(self, fields=[], soundfile=None):
        self.soundfile = soundfile
        self.fields = fields


class soundcloud(MetadataListDirective):
    """Directive used to create fieldsets
    """
    key = SOUNDCLOUD_KEY

    def factory(self, *args):
        metainfo = SoundcloudMeta(fields=args)
        return [metainfo]


class soundfile(MetadataListDirective):
    """Directive used to create fieldsets
    """
    key = SOUNDFILE_KEY

    def factory(self, filefield):
        metainfo = SoundcloudMeta(soundfile=soundfile)
        return [metainfo]
