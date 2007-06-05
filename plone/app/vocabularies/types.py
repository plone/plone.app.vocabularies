from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary

class PortalTypesVocabulary(object):
    """Vocabulary factory for portal types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ttool = getToolByName(context, 'portal_types')
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
        context = getattr(context, 'context', context)
        ptool = getToolByName(context, 'plone_utils')
        ttool = getToolByName(context, 'portal_types')
        items = [ (ttool[t].Title(), t)
                  for t in ptool.getUserFriendlyTypes() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)

UserFriendlyTypesVocabularyFactory = UserFriendlyTypesVocabulary()
