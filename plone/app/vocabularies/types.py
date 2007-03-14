from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from Products.Archetypes.mimetype_utils import getAllowableContentTypes
from Products.Archetypes.mimetype_utils import getAllowedContentTypes

from Products.CMFCore.interfaces import ITypesTool
from Products.CMFPlone.interfaces import IPloneTool


class AllowableContentTypesVocabulary(object):
    """Vocabulary factory for allowable content types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        items = [ (t, t) for t in getAllowableContentTypes(context)]
        items.sort()
        return SimpleVocabulary.fromItems(items)

AllowableContentTypesVocabularyFactory = AllowableContentTypesVocabulary()


class AllowedContentTypesVocabulary(object):
    """Vocabulary factory for allowed content types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        items = [ (t, t) for t in getAllowedContentTypes(context)]
        items.sort()
        return SimpleVocabulary.fromItems(items)

AllowedContentTypesVocabularyFactory = AllowedContentTypesVocabulary()


class PortalTypesVocabulary(object):
    """Vocabulary factory for portal types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        ttool = getUtility(ITypesTool)
        items = [ (ttool[t].Title(), t)
                  for t in ttool.listContentTypes() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)

PortalTypesVocabularyFactory = PortalTypesVocabulary()


class UserFriendlyTypesVocabulary(object):
    """Vocabulary factory for user friendly portal types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        ptool = getUtility(IPloneTool)
        ttool = getUtility(ITypesTool)
        items = [ (ttool[t].Title(), t)
                  for t in ptool.getUserFriendlyTypes() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)

UserFriendlyTypesVocabularyFactory = UserFriendlyTypesVocabulary()
