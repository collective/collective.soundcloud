from zope import schema
from zope.i18nmessageid import MessageFactory
from five import grok
from plone.directives import form, dexterity

_ = MessageFactory("collective.soundcloud")


class ITrack(form.Schema):
    """A soundcloud track. Track can be added anywhere.
    """
    
    title = schema.TextLine(
            title=_(u"Name"),
        )
    