from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.vocabularies import queryVocabulary
from plone.app.vocabularies import vocabulary
from plone.app.vocabularies.testing import PAVocabularies_FUNCTIONAL_TESTING
from zExceptions import Unauthorized
from zope.schema.vocabulary import SimpleVocabulary

import unittest


@vocabulary("plone.app.vocabularies.myvocabulary")
def fooVocabularyFactory(context=None):
    """Provide vocabulary factory.
    """
    terms = []
    for el in ['red', 'blue']:
        terms.append(SimpleVocabulary.createTerm(el, el, el))
    return SimpleVocabulary(terms)


@vocabulary(
    "plone.app.vocabularies.myprotectedvocabulary",
    permission="Modify portal content"
)
def fooProtectedVocabularyFactory(context=None):
    """Provide vocabulary factory.
    """
    terms = []
    for el in ['orange', 'pink']:
        terms.append(SimpleVocabulary.createTerm(el, el, el))
    return SimpleVocabulary(terms)


@vocabulary("plone.app.vocabularies.myvocabulary")
def foo2VocabularyFactory(context=None):
    """Provide vocabulary factory.
    """
    terms = []
    for el in ['magenta', 'purple']:
        terms.append(SimpleVocabulary.createTerm(el, el, el))
    return SimpleVocabulary(terms)


class ProtectedVocabulariesTest(unittest.TestCase):
    layer = PAVocabularies_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_vocabularies_listing(self):
        """Get list of vocabularies.

        TODO TOBEDISCUSSED Should the listing of vocabularies be protected?
        """
        # setRoles(self.portal, TEST_USER_ID, ["Anonymous"])
        # with self.assertRaises(Unauthorized):
        #     queryVocabulary()

        # setRoles(self.portal, TEST_USER_ID, ["Editor"])
        self.assertTrue(
            'plone.app.vocabularies.myprotectedvocabulary' in queryVocabulary()
        )

    def test_vocabulary_protection(self):
        """Get vocabulary of name"""
        setRoles(self.portal, TEST_USER_ID, ["Authenticated"])

        # unprotected vocabulary
        my_vocabulary = queryVocabulary('plone.app.vocabularies.myvocabulary')
        self.assertEqual(
            sorted(list(my_vocabulary().by_token.keys())),
            ['blue', 'red']
        )

        # protected vocabulary
        with self.assertRaises(Unauthorized):
            queryVocabulary('plone.app.vocabularies.myprotectedvocabulary')

        setRoles(self.portal, TEST_USER_ID, ["Editor"])
        my_protected_vocabulary = queryVocabulary(
            'plone.app.vocabularies.myprotectedvocabulary')
        self.assertEqual(
            list(my_protected_vocabulary().by_token.keys()),
            ['orange', 'pink']
        )
