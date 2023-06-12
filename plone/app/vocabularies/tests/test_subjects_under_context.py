from plone.app.vocabularies.testing import PAVocabularies_INTEGRATION_TESTING
from plone.base.interfaces import INavigationRoot
from unittest import mock
from zope.interface import alsoProvides

import unittest


class TestKeywordsUnderContext(unittest.TestCase):
    layer = PAVocabularies_INTEGRATION_TESTING

    def setUp(self):
        """Custom setup for tests."""
        self.portal = self.layer["portal"]

        from plone.app.vocabularies.tests import base

        context = base.create_context()
        rids = (
            "1",
            "2",
        )
        tool = base.DummyCatalog(rids)
        context.portal_catalog = tool
        context.portal_url = base.DummyUrlTool(context)

        from Products.PluginIndexes.KeywordIndex.KeywordIndex import (  # noqa
            KeywordIndex,
        )

        kwindex = KeywordIndex("Subject")
        tool.indexes["Subject"] = kwindex
        from Products.ExtendedPathIndex.ExtendedPathIndex import (  # noqa
            ExtendedPathIndex,
        )

        pathindex = ExtendedPathIndex("path")
        tool.indexes["path"] = pathindex

        self.subjects_1 = ["Berlin", "Wien", "Paris", "Barcelona"]
        self.subjects_2 = ["Montreal", "Washington", "Brasilia"]

        self.navroot1 = base.DummyContentWithParent("nr1", parent=context)
        alsoProvides(self.navroot1, INavigationRoot)
        self.navroot2 = base.DummyContentWithParent("nr2", parent=context)
        alsoProvides(self.navroot2, INavigationRoot)

        self.doc1 = base.DummyContentWithParent(
            "doc1", subjects=self.subjects_1, parent=self.navroot1
        )
        kwindex._index_object(1, self.doc1, attr="Subject")
        pathindex.index_object(1, self.doc1)

        self.doc2 = base.DummyContentWithParent(
            "doc2", subjects=self.subjects_2, parent=self.navroot2
        )
        kwindex._index_object(2, self.doc2, attr="Subject")
        pathindex.index_object(2, self.doc2)

        from plone.app.vocabularies.catalog import KeywordsVocabulary

        self.vocab = KeywordsVocabulary()

        # mock our registry
        from plone.registry import Registry
        from plone.registry.interfaces import IRegistry
        from zope.component import getSiteManager

        sm = getSiteManager()
        from Products.CMFCore.interfaces import ICatalogTool

        sm.registerUtility(tool, ICatalogTool)
        registry = Registry()
        sm.registerUtility(registry, IRegistry)
        from Products.CMFCore.interfaces import IURLTool

        sm.registerUtility(context.portal_url, IURLTool)
        registry_patcher = mock.patch("plone.registry.registry.Registry.get")
        self.addCleanup(registry_patcher.stop)
        self.registry_mock = registry_patcher.start()

    def test_all_kw(self):
        self.registry_mock.return_value = False
        self.assertEqual(len(self.vocab(self.doc1)), 7)
        self.assertEqual(len(self.vocab(self.doc2)), 7)

    def test_all_kw_none_setting(self):
        self.registry_mock.return_value = None
        self.assertEqual(len(self.vocab(self.doc1)), 7)
        self.assertEqual(len(self.vocab(self.doc2)), 7)

    def test_keywords_of_navroot(self):
        self.registry_mock.return_value = True
        self.assertEqual(len(self.vocab(self.doc1)), 4)
        self.assertEqual(len(self.vocab(self.doc2)), 3)
