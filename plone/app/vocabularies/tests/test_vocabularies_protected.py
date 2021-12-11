from plone.app.vocabularies.registry import IVocabularyRegistry
from plone.app.vocabularies.testing import PAVocabularies_FUNCTIONAL_TESTING
from plone.app.vocabularies.testing import setRoles
from plone.app.vocabularies.testing import TEST_USER_ID
from zExceptions import Unauthorized
from zope.component import queryUtility
from zope.schema.vocabulary import SimpleVocabulary

import unittest


def fooVocabularyFactory(context=None):
    """Provide vocabulary factory.
    """
    terms = []
    for el in ['red', 'blue']:
        terms.append(SimpleVocabulary.createTerm(el, el, el))
    return SimpleVocabulary(terms)


def fooProtectedVocabularyFactory(context=None):
    """Provide vocabulary factory.
    """
    terms = []
    for el in ['orange', 'pink']:
        terms.append(SimpleVocabulary.createTerm(el, el, el))
    return SimpleVocabulary(terms)


class ProtectedVocabulariesTest(unittest.TestCase):
    layer = PAVocabularies_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        vocabularyRegistry = queryUtility(IVocabularyRegistry)
        vocabularyRegistry.registerVocabulary(
            name="plone.app.vocabularies.myvocabulary",
            factory=fooVocabularyFactory
        )
        vocabularyRegistry.registerVocabulary(
            name="plone.app.vocabularies.myprotectedvocabulary",
            factory=fooProtectedVocabularyFactory,
            permission="Modify portal content"
        )

    def test_vocabularies_listing(self):
        """Get list of vocabularies.

        TODO TOBEDISCUSSED Should the listing of vocabularies be protected?
        """

        vocabularyRegistry = queryUtility(IVocabularyRegistry)
        self.assertTrue(
            'plone.app.vocabularies.myprotectedvocabulary'
            in vocabularyRegistry.queryVocabulary()
        )

    def test_vocabulary_protection(self):
        """Get vocabulary of name"""
        setRoles(self.portal, TEST_USER_ID, ["Authenticated"])

        vocabularyRegistry = queryUtility(IVocabularyRegistry)

        # unprotected vocabulary
        my_vocabulary = vocabularyRegistry.queryVocabulary(
            'plone.app.vocabularies.myvocabulary'
        )
        self.assertEqual(
            sorted(list(my_vocabulary().by_token.keys())),
            ['blue', 'red']
        )

        # protected vocabulary
        with self.assertRaises(Unauthorized):
            vocabularyRegistry.queryVocabulary(
                'plone.app.vocabularies.myprotectedvocabulary'
            )

        setRoles(self.portal, TEST_USER_ID, ["Editor"])
        my_protected_vocabulary = vocabularyRegistry.queryVocabulary(
            'plone.app.vocabularies.myprotectedvocabulary')
        self.assertEqual(
            list(my_protected_vocabulary().by_token.keys()),
            ['orange', 'pink']
        )

    def test_vocabulary_zcml_registration(self):
        """Get vocabulary of name"""
        setRoles(self.portal, TEST_USER_ID, ["Authenticated"])

        vocabularyRegistry = queryUtility(IVocabularyRegistry)

        # unprotected vocabulary
        my_vocabulary = vocabularyRegistry.queryVocabulary(
            'plone.app.vocabularies.testzeceeml'
        )
        self.assertTrue(my_vocabulary is not None)
        self.assertEqual(
            sorted(list(my_vocabulary().by_token.keys())),
            ['blue', 'red']
        )

        # protected vocabulary
        with self.assertRaises(Unauthorized):
            vocabularyRegistry.queryVocabulary(
                'plone.app.vocabularies.testzeceemlprotected'
            )

        setRoles(self.portal, TEST_USER_ID, ["Editor"])
        my_protected_vocabulary = vocabularyRegistry.queryVocabulary(
            'plone.app.vocabularies.testzeceemlprotected')
        self.assertEqual(
            list(my_protected_vocabulary().by_token.keys()),
            ['orange', 'pink']
        )
