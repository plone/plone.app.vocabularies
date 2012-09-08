from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFPlone.interfaces.syndication import ISiteSyndicationSettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.interface.topic import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces._content import IFolderish

_ = MessageFactory('plone')


class SyndicationFeedTypesVocabulary(object):
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


class SyndicatableFeedItems(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')
        site_path = '/'.join(site.getPhysicalPath())
        query = {
            'portal_type': ('Folder', 'Collection', 'Topic'),
            'path': {"query": site_path,
                     'depth': 2}
        }
        items = []
        for brain in catalog(**query):
            uid = brain.UID
            title = '%s(%s)' % (brain.Title,
                                brain.getPath()[len(site_path) + 1:])
            items.append(SimpleTerm(uid, uid, title))
        return SimpleVocabulary(items)

SyndicatableFeedItemsFactory = SyndicatableFeedItems()
