import unittest

import zope.component
from zope.component.testing import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig
from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite

import plone.app.vocabularies

def configurationSetUp(self):
    setUp()
    XMLConfig('meta.zcml', zope.component)()
    XMLConfig('configure.zcml', plone.app.vocabularies)()


def test_suite():
    return unittest.TestSuite((
        DocTestSuite('plone.app.vocabularies.catalog',
                     setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.groups',
                     setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.language',
                     setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.security',
                     setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.skins',
                     setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.terms'),
        DocTestSuite('plone.app.vocabularies.types',
                     setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.users',
                     setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        DocTestSuite('plone.app.vocabularies.workflow',
                     setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
