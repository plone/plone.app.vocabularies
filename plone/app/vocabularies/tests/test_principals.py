# -*- coding: utf-8 -*-
from plone.app.vocabularies.testing import PAVocabularies_INTEGRATION_TESTING
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TimezoneTest(unittest.TestCase):
    layer = PAVocabularies_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

