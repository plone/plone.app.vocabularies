from operator import itemgetter
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class AvailableContentLanguageVocabulary:
    """Vocabulary factory for available content languages in the portal.

    >>> from zope.component import queryUtility
    >>> from plone.app.vocabularies.tests.base import create_context
    >>> from plone.app.vocabularies.tests.base import DummyTool

    >>> name = 'plone.app.vocabularies.AvailableContentLanguages'
    >>> util = queryUtility(IVocabularyFactory, name)
    >>> context = create_context()

    >>> len(util(context))  # 'en' is given as default now
    1

    >>> tool = DummyTool('portal_languages')
    >>> def getAvailableLanguages():
    ...     return dict(en=dict(name='English', native='English'),
    ...                 de=dict(name='German', native='Deutsch'))
    >>> tool.getAvailableLanguages = getAvailableLanguages
    >>> context.portal_languages = tool

    >>> languages = util(context)
    >>> languages
    <zope.schema.vocabulary.SimpleVocabulary object at ...>

    >>> len(languages.by_token)
    2

    >>> de = languages.by_token['de']
    >>> de.title, de.token, de.value
    ('Deutsch', 'de', 'de')
    """

    def __call__(self, context):
        items = [SimpleTerm("en", "en", "English")]  # default, only english
        site = getSite()
        ltool = getToolByName(site, "portal_languages", None)
        if ltool is not None:
            languages = ltool.getAvailableLanguages()
            items = [(lang, languages[lang].get("native", lang)) for lang in languages]
            items.sort(key=itemgetter(1))
            items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)


AvailableContentLanguageVocabularyFactory = AvailableContentLanguageVocabulary()  # noqa


@implementer(IVocabularyFactory)
class SupportedContentLanguageVocabulary:
    """Vocabulary factory for supported content languages in the portal.

    >>> from zope.component import queryUtility
    >>> from plone.app.vocabularies.tests.base import create_context
    >>> from plone.app.vocabularies.tests.base import DummyTool

    >>> name = 'plone.app.vocabularies.SupportedContentLanguages'
    >>> util = queryUtility(IVocabularyFactory, name)
    >>> context = create_context()

    >>> len(util(context))
    0

    >>> tool = DummyTool('portal_languages')
    >>> def listSupportedLanguages():
    ...     return [('en', 'English'), ('de', 'German')]
    >>> tool.listSupportedLanguages = listSupportedLanguages
    >>> def getAvailableLanguages():
    ...     return dict(en=dict(name='English', native='English'),
    ...                 de=dict(name='German', native='Deutsch'))
    >>> tool.getAvailableLanguages = getAvailableLanguages
    >>> context.portal_languages = tool

    >>> languages = util(context)
    >>> languages
    <zope.schema.vocabulary.SimpleVocabulary object at ...>

    >>> len(languages.by_token)
    2

    >>> de = languages.by_token['de']
    >>> de.title, de.token, de.value
    ('Deutsch', 'de', 'de')
    """

    def __call__(self, context):
        items = []
        site = getSite()
        ltool = getToolByName(site, "portal_languages", None)
        if ltool is not None:
            items = ltool.listSupportedLanguages()
            all_langs = ltool.getAvailableLanguages()
            items = [
                (lang[0], all_langs[lang[0]].get("native", lang[1])) for lang in items
            ]
            items.sort(key=itemgetter(1))
            items = [
                SimpleTerm(i[0], i[0], all_langs.get(i[0], {}).get("native", i[1]))
                for i in items
            ]
        return SimpleVocabulary(items)


SupportedContentLanguageVocabularyFactory = SupportedContentLanguageVocabulary()  # noqa
