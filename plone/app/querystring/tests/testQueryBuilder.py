from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest

from base import QuerystringTestCase


class TestQuerybuilder(QuerystringTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Document",
                                  "collectionstestpage",
                                  title="Collectionstestpage")
        testpage = self.portal['collectionstestpage']
        self.portal.portal_workflow.doActionFor(testpage, 'publish')
        self.request = TestRequest()
        self.querybuilder = getMultiAdapter((self.portal, self.request),
                                             name='querybuilderresults')
        self.query = [{
            'i': 'Title',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Collectionstestpage',
        }]

    def testQueryBuilderQuery(self):
        results = self.querybuilder(query=self.query)
        self.assertEqual(results[0].Title(), "Collectionstestpage")

    def testQueryBuilderHTML(self):
        results = self.querybuilder.html_results(self.query)
        self.failUnless('Collectionstestpage' in results)

    def testGettingConfiguration(self):
        res = self.folder.restrictedTraverse('@@querybuildernumberofresults')
        res(self.query)


class TestConfigurationFetcher(QuerystringTestCase):

    def testGettingJSONConfiguration(self):
        self.folder.restrictedTraverse('@@querybuilderjsonconfig')()
