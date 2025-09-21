from plone.app.vocabularies.containers import RestoreContainersVocabularyFactory
from plone.app.vocabularies.testing import PAVocabularies_INTEGRATION_TESTING

import unittest


class RestoreContainersVocabularyTest(unittest.TestCase):
    """Test the RestoreContainersVocabulary"""

    layer = PAVocabularies_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_vocabulary_factory(self):
        """Test that the vocabulary factory is callable"""
        vocab_factory = RestoreContainersVocabularyFactory
        vocab = vocab_factory(self.portal)
        self.assertIsNotNone(vocab)

    def test_vocabulary_contains_site_root(self):
        """Test that the vocabulary contains the site root"""
        vocab_factory = RestoreContainersVocabularyFactory
        vocab = vocab_factory(self.portal)
        terms = list(vocab)
        self.assertTrue(len(terms) > 0)
        # First term should be the site root
        first_term = terms[0]
        self.assertEqual(first_term.title, "/ (Site Root)")

    def test_vocabulary_contains_folders(self):
        """Test that the vocabulary contains folderish items"""
        # Create a folder
        self.portal.invokeFactory("Folder", "test-folder", title="Test Folder")

        vocab_factory = RestoreContainersVocabularyFactory
        vocab = vocab_factory(self.portal)
        terms = list(vocab)

        # Should contain at least the site root and our test folder
        self.assertTrue(len(terms) >= 2)

        # Find our test folder in the vocabulary
        folder_terms = [term for term in terms if "Test Folder" in term.title]
        self.assertTrue(len(folder_terms) > 0)
