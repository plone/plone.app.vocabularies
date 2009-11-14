from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName

def sort_key(language):
    return language[1]


class AvailableContentLanguageVocabulary(object):
    """Vocabulary factory for available content languages in the portal.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.AvailableContentLanguages'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> tool = DummyTool('portal_languages')
      >>> def getAvailableLanguages():
      ...     return dict(en=dict(name='English'),
      ...                 de=dict(name='German'))
      >>> tool.getAvailableLanguages = getAvailableLanguages
      >>> context2.portal_languages = tool

      >>> languages = util(context1)
      >>> languages
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(languages.by_token)
      2

      >>> de = languages.by_token['de']
      >>> de.title, de.token, de.value
      ('German', 'de', 'de')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ltool = getToolByName(context, 'portal_languages', None)
        if ltool is None:
            return None
        languages = ltool.getAvailableLanguages()
        items = [(l, languages[l].get('name', l)) for l in languages]
        items.sort(key=sort_key)
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)

AvailableContentLanguageVocabularyFactory = AvailableContentLanguageVocabulary()


class SupportedContentLanguageVocabulary(object):
    """Vocabulary factory for supported content languages in the portal.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.SupportedContentLanguages'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> tool = DummyTool('portal_languages')
      >>> def listSupportedLanguages():
      ...     return [('en', 'English'), ('de', 'German')]
      >>> tool.listSupportedLanguages = listSupportedLanguages
      >>> context2.portal_languages = tool

      >>> languages = util(context1)
      >>> languages
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(languages.by_token)
      2

      >>> de = languages.by_token['de']
      >>> de.title, de.token, de.value
      ('German', 'de', 'de')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ltool = getToolByName(context, 'portal_languages', None)
        if ltool is None:
            return None
        items = ltool.listSupportedLanguages()
        items.sort(key=sort_key)
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)

SupportedContentLanguageVocabularyFactory = SupportedContentLanguageVocabulary()
