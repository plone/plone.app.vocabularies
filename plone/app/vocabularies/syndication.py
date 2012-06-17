from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFPlone.interfaces.syndication import ISiteSyndicationSettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

_ = MessageFactory('plone')


class SyndicationFeedTypesVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSyndicationSettings)
        items = []
        for _type in settings.allowed_feed_types:
            split = _type.split('|')
            if len(split) == 2:
                name, title = split
                items.append(SimpleTerm(name, name, title))
        return SimpleVocabulary(items)

SyndicationFeedTypesVocabularyFactory = SyndicationFeedTypesVocabulary()
