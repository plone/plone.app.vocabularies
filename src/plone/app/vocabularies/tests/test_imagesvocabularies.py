from plone.app.vocabularies.testing import PAVocabularies_INTEGRATION_TESTING
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class ImagesTest(unittest.TestCase):
    layer = PAVocabularies_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_images_scales_vocabulary(self):
        images_scales_voc = getUtility(
            IVocabularyFactory, "plone.app.vocabularies.ImagesScales"
        )
        scales_list = [item.value for item in images_scales_voc(self.portal)]
        self.assertTrue("thumb" in scales_list)
        self.assertTrue("large" in scales_list)
        self.assertTrue("preview" in scales_list)
