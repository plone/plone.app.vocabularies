import unittest
from zope.testing.doctestunit import DocTestSuite

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('plone.app.vocabularies.catalog'),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
