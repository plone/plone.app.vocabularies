from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.interfaces import ISkinsTool


class SkinsVocabulary(object):
    """Vocabulary factory for skins.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        stool = getUtility(ISkinsTool)
        items = [ (s, s)
                  for s in stool.getSkinSelections() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)

SkinsVocabularyFactory = SkinsVocabulary()
