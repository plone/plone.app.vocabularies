# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

try:
    # XXX: this is a circular dependency (not declared in setup.py)
    from Products.CMFPlone.interfaces.syndication import ISiteSyndicationSettings  # noqa
    HAS_SYNDICATION = True
except ImportError:
    # new syndication not available
    HAS_SYNDICATION = False

_ = MessageFactory('plone')


@implementer(IVocabularyFactory)
class SyndicationFeedTypesVocabulary(object):

    def __call__(self, context):
        if not HAS_SYNDICATION:
            return SimpleVocabulary([])
        registry = getUtility(IRegistry)
        try:
            settings = registry.forInterface(ISiteSyndicationSettings)
        except KeyError:
            return SimpleVocabulary([])
        items = []
        for _type in settings.allowed_feed_types:
            split = _type.split('|')
            if len(split) == 2:
                name, title = split
                items.append(SimpleTerm(name, name, title))
        return SimpleVocabulary(items)

SyndicationFeedTypesVocabularyFactory = SyndicationFeedTypesVocabulary()


@implementer(IVocabularyFactory)
class SyndicatableFeedItems(object):

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
            title = u'%s(%s)' % (brain.Title.decode('utf8'),
                                 brain.getPath()[len(site_path) + 1:])
            items.append(SimpleTerm(uid, uid, title))
        return SimpleVocabulary(items)

SyndicatableFeedItemsFactory = SyndicatableFeedItems()
