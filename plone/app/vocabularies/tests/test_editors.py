from plone.app.vocabularies.testing import PAVocabularies_INTEGRATION_TESTING
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class AvailableEditorsTest(unittest.TestCase):

    layer = PAVocabularies_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_editors(self):
        from plone.registry import Registry

        registry = Registry()
        from plone.base.interfaces import IEditingSchema

        registry.registerInterface(IEditingSchema, prefix="plone")
        registry.records["plone.available_editors"]
        vocab_util = getUtility(
            IVocabularyFactory, "plone.app.vocabularies.AvailableEditors"
        )
        editors = vocab_util(self.portal)
        self.assertEqual(2, len(editors.by_token))
        self.assertTrue("None" in [x for x in editors.by_token])
        self.assertTrue("TinyMCE" in [x for x in editors.by_token])
