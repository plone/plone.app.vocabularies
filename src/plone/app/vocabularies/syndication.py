from plone.base.interfaces import ISiteSyndicationSettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class SyndicationFeedTypesVocabulary:
    def __call__(self, context):
        registry = getUtility(IRegistry)
        try:
            settings = registry.forInterface(ISiteSyndicationSettings)
        except KeyError:
            return SimpleVocabulary([])
        items = []
        for _type in settings.allowed_feed_types:
            split = _type.split("|")
            if len(split) == 2:
                name, title = split
                items.append(SimpleTerm(name, name, title))
        return SimpleVocabulary(items)


SyndicationFeedTypesVocabularyFactory = SyndicationFeedTypesVocabulary()


@implementer(IVocabularyFactory)
class SyndicatableFeedItems:
    def __call__(self, context):
        site = getSite()
        catalog = getToolByName(site, "portal_catalog")
        site_path = "/".join(site.getPhysicalPath())
        query = {
            "portal_type": ("Folder", "Collection", "Topic"),
            "path": {"query": site_path, "depth": 2},
        }
        items = []
        for brain in catalog(**query):
            uid = brain.UID
            title = brain.Title
            if isinstance(title, bytes):
                title = title.decode("utf8")
            title = "{}({})".format(
                title,
                brain.getPath()[len(site_path) + 1 :],
            )
            items.append(SimpleTerm(uid, uid, title))
        return SimpleVocabulary(items)


SyndicatableFeedItemsFactory = SyndicatableFeedItems()
