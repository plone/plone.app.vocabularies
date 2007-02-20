from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName


class SkinsVocabulary(object):
    """Vocabulary factory for skins.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        stool = getToolByName(context, 'portal_skins')
        items = [ (s, s)
                  for s in stool.getSkinSelections() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)

SkinsVocabularyFactory = SkinsVocabulary()
