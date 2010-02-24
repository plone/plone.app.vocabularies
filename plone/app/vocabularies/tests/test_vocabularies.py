import unittest

import zope.component
from zope.component.testing import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig
from zope.site import hooks
from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite

import plone.app.vocabularies


def vocabSetUp(self):
    setUp()
    XMLConfig('meta.zcml', zope.component)()
    XMLConfig('configure.zcml', plone.app.vocabularies)()
    hooks.setHooks()


def vocabTearDown(self):
    tearDown()
    hooks.resetHooks()
    hooks.setSite()


def test_suite():
    return unittest.TestSuite((
        DocTestSuite('plone.app.vocabularies.catalog',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.groups',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.language',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.security',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.skins',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.terms'),
        DocTestSuite('plone.app.vocabularies.types',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.users',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.workflow',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
       DocTestSuite('plone.app.vocabularies.editors',
                     setUp=vocabSetUp,
                     tearDown=vocabTearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
