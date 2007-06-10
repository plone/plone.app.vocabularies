from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from Products.CMFCore.utils import getToolByName

def sort_key(language):
    return language[1]


class AvailableContentLanguageVocabulary(object):
    """Vocabulary factory for available content languages in the portal.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ltool = getToolByName(context, 'portal_languages')
        languages = ltool.getAvailableLanguages()
        items = [(l, languages[l].get('name', l)) for l in languages]
        items.sort(key=sort_key)
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)

AvailableContentLanguageVocabularyFactory = AvailableContentLanguageVocabulary()


class SupportedContentLanguageVocabulary(object):
    """Vocabulary factory for supported content languages in the portal.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ltool = getToolByName(context, 'portal_languages')
        items = ltool.listSupportedLanguages()
        items.sort(key=sort_key)
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)

SupportedContentLanguageVocabularyFactory = SupportedContentLanguageVocabulary()
