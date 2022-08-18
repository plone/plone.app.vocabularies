from doctest import DocTestSuite
from zope.component import hooks
from zope.component.testing import setUp
from zope.component.testing import tearDown
from zope.configuration.xmlconfig import XMLConfig

import doctest
import re
import unittest
import zope.component


def vocabSetUp(self):
    setUp()
    import plone.app.vocabularies

    XMLConfig("meta.zcml", zope.component)()
    XMLConfig("configure.zcml", plone.app.vocabularies)()
    hooks.setHooks()


def vocabTearDown(self):
    tearDown()
    hooks.resetHooks()
    hooks.setSite()


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        want = re.sub("u'(.*?)'", "'\\1'", want)
        want = re.sub('u"(.*?)"', '"\\1"', want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    return unittest.TestSuite(
        (
            DocTestSuite("plone.app.vocabularies.terms"),
            DocTestSuite(
                "plone.app.vocabularies.catalog",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.datetimerelated",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.groups",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.language",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.metadatafields",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.security",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.skins",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.types",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.users",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
            DocTestSuite(
                "plone.app.vocabularies.workflow",
                setUp=vocabSetUp,
                tearDown=vocabTearDown,
                optionflags=optionflags,
                checker=Py23DocChecker(),
            ),
        )
    )
