# -*- coding: utf-8 -*-
from collective.soundcloud import _
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import directlyProvides


def TrackTypesVocabulary(context):
    types = [
        ('original'),
        ('remix'),
        ('live'),
        ('recording'),
        ('spoken'),
        ('podcast'),
        ('demo'),
        ('in progress'),
        ('stem'),
        ('loop'),
        ('sound effect'),
        ('sample'),
        ('other'),
    ]
    terms = [SimpleTerm(term, term, title=term) for term in types]
    return SimpleVocabulary(terms)

directlyProvides(TrackTypesVocabulary, IVocabularyFactory)


def LicensesVocabulary(context):
    types = [
        ('no-rights-reserved'),
        ('all-rights-reserved'),
        ('cc-by'),
        ('cc-by-nc'),
        ('cc-by-nd'),
        ('cc-by-sa'),
        ('cc-by-nc-nd'),
        ('cc-by-nc-sa'),
    ]
    terms = [SimpleTerm(term, term, title=term) for term in types]
    return SimpleVocabulary(terms)

directlyProvides(LicensesVocabulary, IVocabularyFactory)


def SharingVocabulary(context):
    types = [
        ('public',
            _(
                'public',
                default=u'Public - Makes this track  available to everyone'
            )
         ),
        ('private',
            _('private', default=u'Private - Only you have access')
         ),
    ]
    terms = [SimpleTerm(term, term, title=label) for term, label in types]
    return SimpleVocabulary(terms)

directlyProvides(SharingVocabulary, IVocabularyFactory)


def DownloadVocabulary(context):
    types = [
        ('true', _('true', default=u'Enabled')),
        ('false', _('false', default=u'Disabled')),
    ]
    terms = [SimpleTerm(term, term, title=label) for term, label in types]
    return SimpleVocabulary(terms)

directlyProvides(DownloadVocabulary, IVocabularyFactory)

