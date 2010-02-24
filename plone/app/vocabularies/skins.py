from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName


class SkinsVocabulary(object):
    """Vocabulary factory for skins.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.Skins'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> tool = DummyTool('portal_skins')
      >>> def getSkinSelections():
      ...     return ('Plone Default', 'Plone Kitty')
      >>> tool.getSkinSelections = getSkinSelections
      >>> context2.portal_skins = tool

      >>> skins = util(context1)
      >>> skins
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(skins.by_token)
      2

      >>> de = skins.by_token['Plone Kitty']
      >>> de.title, de.token, de.value
      ('Plone Kitty', 'Plone Kitty', 'Plone Kitty')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        stool = getToolByName(context, 'portal_skins', None)
        if stool is None:
            return None
        items = list(stool.getSkinSelections())
        items.sort()
        items = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(items)

SkinsVocabularyFactory = SkinsVocabulary()
