 # -*- coding: utf-8 -*-

from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest

from .base import QuerystringTestCase


class TestQuerybuilder(QuerystringTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Document",
                                  "collectionstestpage",
                                  title="Collectionstestpage")
        testpage = self.portal['collectionstestpage']
        self.testpage = testpage
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
        self.assertTrue('Collectionstestpage' in results)

    def testGettingConfiguration(self):
        res = self.folder.restrictedTraverse('@@querybuildernumberofresults')
        res(self.query)

    def testQueryBuilderNumberOfResults(self):
        results = self.querybuilder.number_of_results(self.query)
        numeric = int(results.split(' ')[0])
        self.assertEqual(numeric, 1)

    def testQueryBuilderNumberOfResultsView(self):
        res = self.folder.restrictedTraverse('@@querybuildernumberofresults')
        length_of_results = res.browserDefault(None)[0](self.query)
        # apparently brower travelsal is different from the traversal we get
        # from restrictedTraverse. This did hurt a bit.
        numeric = int(length_of_results.split(' ')[0])
        self.assertEqual(numeric, 1)

    def testMakeQuery(self):
        results = self.querybuilder._makequery(query=self.query)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].getURL(),
            'http://nohost/plone/collectionstestpage')

    def testMakeQueryWithSubject(self):
        self.testpage.setSubject(['Lorem'])
        self.testpage.reindexObject()
        query = [{
            'i': 'Subject',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'Lorem',
        }]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].getURL(),
            'http://nohost/plone/collectionstestpage')

    def testMakeQueryWithMultipleSubject(self):
        self.testpage.setSubject(['Lorem'])
        self.testpage.reindexObject()
        query = [{
            'i': 'Subject',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': ['Lorem', 'Ipsum'],
        }]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].getURL(),
            'http://nohost/plone/collectionstestpage')

    def testMakeQueryWithSubjectWithSpecialCharacters(self):
        self.testpage.setSubject(['Äüö'])
        self.testpage.reindexObject()
        query = [{
            'i': 'Subject',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'Äüö',
        }]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].getURL(),
            'http://nohost/plone/collectionstestpage')
        self.assertEqual(
            results[0].getObject().Subject(),
            ('Äüö',))

    def testMakeQueryWithUnicodeSubjectWithSpecialCharacters(self):
        self.testpage.setSubject(['Äüö'])
        self.testpage.reindexObject()
        query = [{
            'i': 'Subject',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': u'Äüö',
        }]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].getURL(),
            'http://nohost/plone/collectionstestpage')
        self.assertEqual(
            results[0].getObject().Subject(),
            ('Äüö',))

    def testMakeQueryWithUnicodeSubjectWithMultipleSubjects(self):
        self.testpage.setSubject(['Äüö'])
        self.testpage.reindexObject()
        query = [{
            'i': 'Subject',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': [u'Äüö', u'Üöß'],
        }]
        results = self.querybuilder._makequery(query=query)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].getURL(),
            'http://nohost/plone/collectionstestpage')
        self.assertEqual(
            results[0].getObject().Subject(),
            ('Äüö',))


class TestConfigurationFetcher(QuerystringTestCase):

    def testGettingJSONConfiguration(self):
        self.folder.restrictedTraverse('@@querybuilderjsonconfig')()
