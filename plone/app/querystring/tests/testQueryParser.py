import unittest

from DateTime import DateTime
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.querystring import queryparser
from plone.registry import field
from plone.registry import Record

from .base import UnittestWithRegistryLayer
from plone.app.querystring.queryparser import Row
from zope.interface.declarations import implements

MOCK_SITE_ID = "site"


class MockObject(object):

    def __init__(self, uid, path):
        self.uid = uid
        self.path = path.split("/")

    def getPath(self):
        return self.path

    def getPhysicalPath(self):
        return self.path

    def absolute_url(self):
        return self.path


class MockCatalog(object):

    def unrestrictedSearchResults(self, query):
        uid = query.get('UID')
        if uid == '00000000000000001':
            return [MockObject(uid='00000000000000001',
                               path="/%s/foo" % MOCK_SITE_ID)]
        raise NotImplementedError

    def indexes(self):
        return ['Title', 'effectiveRange', 'object_provides',
                'end', 'Description', 'is_folderish', 'getId',
                'start', 'meta_type', 'is_default_page', 'Date',
                'review_state', 'portal_type', 'expires',
                'allowedRolesAndUsers', 'getObjPositionInParent', 'path',
                'UID', 'effective', 'created', 'Creator',
                'modified', 'SearchableText', 'sortable_title',
                'getRawRelatedItems', 'Subject']


class MockPortalUrl(object):

    def getPortalPath(self):
        return "/%s" % MOCK_SITE_ID

    def getPortalObject(self):
        return MockObject(uid='00000000000000000', path="/%s" % MOCK_SITE_ID)


class MockNavtreeProperties(object):

    def getProperty(self, name, default=""):
        return ""


class MockSiteProperties(object):
    navtree_properties = MockNavtreeProperties()


class MockSite(object):
    implements(INavigationRoot)

    def __init__(self, portal_membership=None):
        self.reference_catalog = MockCatalog()
        self.portal_catalog = MockCatalog()
        self.portal_membership = portal_membership
        self.portal_url = MockPortalUrl()
        self.portal_properties = MockSiteProperties()

    def getPhysicalPath(self):
        return ["", MOCK_SITE_ID]


class MockUser(object):

    def __init__(self, username=None):
        self.username = 'Anonymous User'
        if username:
            self.username = username

    def getUserName(self):
        return self.username


class MockPortal_membership(object):

    def __init__(self, user):
        self.user = user

    def getAuthenticatedMember(self):
        return self.user


class TestQueryParserBase(unittest.TestCase):

    layer = UnittestWithRegistryLayer

    def setUp(self):
        super(TestQueryParserBase, self).setUp()
        self.setFunctionForOperation(
            'plone.app.querystring.operation.string.is.operation',
            'plone.app.querystring.queryparser._equal')
        self.setFunctionForOperation(
            'plone.app.querystring.operation.string.path.operation',
            'plone.app.querystring.queryparser._path')

    def setFunctionForOperation(self, operation, function):
        function_field = field.ASCIILine(title=u"Operator")
        function_record = Record(function_field)
        function_record.value = function
        self.layer.registry.records[operation] = function_record


class TestQueryParser(TestQueryParserBase):

    def test_exact_title(self):
        data = {
            'i': 'Title',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Welcome to Plone',
        }
        parsed = queryparser.parseFormquery(MockSite(), [data, ])
        self.assertEqual(parsed, {'Title': {'query': 'Welcome to Plone'}})

    def test_path_explicit(self):
        data = {
            'i': 'path',
            'o': 'plone.app.querystring.operation.string.path',
            'v': '/foo',
        }
        parsed = queryparser.parseFormquery(MockSite(), [data, ])
        self.assertEqual(parsed, {'path': {'query': '/%s/foo' % MOCK_SITE_ID}})

    def test_path_computed(self):
        data = {
            'i': 'path',
            'o': 'plone.app.querystring.operation.string.path',
            'v': '00000000000000001',
        }

        parsed = queryparser.parseFormquery(MockSite(), [data, ])
        self.assertEqual(parsed, {'path': {'query': '/%s/foo' % MOCK_SITE_ID}})


class TestQueryGenerators(TestQueryParserBase):

    def test__between(self):
        data = Row(index='modified',
                  operator='_between',
                  values=['2009/08/12', '2009/08/14'])
        parsed = queryparser._between(MockSite(), data)
        expected = {'modified': {'query': ['2009/08/12', '2009/08/14'],
                    'range': 'minmax'}}
        self.assertEqual(parsed, expected)

    def test__between_reversed_dates(self):
        data = Row(index='modified',
                  operator='_between',
                  values=['2009/08/14', '2009/08/12'])
        parsed = queryparser._between(MockSite(), data)
        expected = {'modified': {'query': ['2009/08/12', '2009/08/14'],
                    'range': 'minmax'}}
        self.assertEqual(parsed, expected)

    def test__largerThan(self):
        data = Row(index='modified',
                  operator='_largerThan',
                  values='2010/03/18')
        parsed = queryparser._largerThan(MockSite(), data)
        expected = {'modified': {'query': '2010/03/18', 'range': 'min'}}
        self.assertEqual(parsed, expected)

    def test__lessThan(self):
        data = Row(index='modified',
                  operator='_lessThan',
                  values='2010/03/18')
        parsed = queryparser._lessThan(MockSite(), data)
        expected = {'modified': {'query': '2010/03/18', 'range': 'max'}}
        self.assertEqual(parsed, expected)

    def test__currentUser(self):
        # Anonymous user
        u = MockUser()
        pm = MockPortal_membership(user=u)
        context = MockSite(portal_membership=pm)
        data = Row(index='Creator',
                  operator='_currentUser',
                  values=None)
        parsed = queryparser._currentUser(context, data)
        expected = {'Creator': {'query': 'Anonymous User'}}
        self.assertEqual(parsed, expected)

        # Logged in user 'admin'
        u = MockUser(username='admin')
        pm = MockPortal_membership(user=u)
        context = MockSite(portal_membership=pm)
        data = Row(index='Creator',
                  operator='_currentUser',
                  values=None)
        parsed = queryparser._currentUser(context, data)
        expected = {'Creator': {'query': 'admin'}}
        self.assertEqual(parsed, expected)

    def test__lessThanRelativeDate(self):
        days = 2
        now = DateTime()
        mydate = now + days
        expected_dates = [now.earliestTime(), mydate.latestTime()]
        expected = {'modified': {'query': expected_dates, 'range': 'minmax'}}
        data = Row(index='modified',
                  operator='_lessThanRelativeDate',
                  values=days)
        parsed = queryparser._lessThanRelativeDate(MockSite(), data)
        self.assertEqual(parsed, expected)

    def test__moreThanRelativeDate(self):
        days = 2
        now = DateTime()
        mydate = now - days
        expected_dates = [mydate.earliestTime(), now.latestTime()]
        expected = {'modified': {'query': expected_dates, 'range': 'minmax'}}
        data = Row(index='modified',
                  operator='_moreThanRelativeDate',
                  values=days)
        parsed = queryparser._moreThanRelativeDate(MockSite(), data)
        self.assertEqual(parsed, expected)

    def test__today(self):
        now = DateTime()
        expected_dates = [now.earliestTime(), now.latestTime()]
        expected = {'modified': {'query': expected_dates, 'range': 'minmax'}}
        data = Row(index='modified',
                  operator='_today',
                  values=expected_dates)
        parsed = queryparser._today(MockSite(), data)
        self.assertEqual(parsed, expected)

    def test__path(self):
        # normal path
        data = Row(index='path',
                  operator='_path',
                  values='/news/')
        parsed = queryparser._path(MockSite(), data)
        expected = {'path': {'query': '/%s/news/' % MOCK_SITE_ID}}
        self.assertEqual(parsed, expected)

        # by uid
        data = Row(index='path',
                  operator='_path',
                  values='00000000000000001')
        parsed = queryparser._path(MockSite(), data)
        expected = {'path': {'query': '/%s/foo' % MOCK_SITE_ID}}
        self.assertEqual(parsed, expected)

    def test__relativePath(self):
        # build test navtree
        context = MockObject(uid='00000000000000001',
                             path="/%s/bar/fizz" % MOCK_SITE_ID)
        context.__parent__ = MockObject(uid='00000000000000002',
                                        path="/%s/bar" % MOCK_SITE_ID)
        # Plone root
        context.__parent__.__parent__ = MockSite()
        # Zope root
        context.__parent__.__parent__.__parent__ = \
            MockObject(uid='00000000000000004', path="/")
        # ploneroot sub folder
        context.__parent__.__parent__.ham = \
            MockObject(uid='00000000000000005',
                       path="/%s/ham" % MOCK_SITE_ID)
        # collection subfolder
        context.__parent__.egg = MockObject(uid='00000000000000006',
                                            path="/%s/bar/egg" % MOCK_SITE_ID)

        # show my siblings
        data = Row(index='path',
                  operator='_relativePath',
                  values='..')
        parsed = queryparser._relativePath(context, data)
        expected = {'path': {'query': '/%s/bar' % MOCK_SITE_ID}}
        self.assertEqual(parsed, expected)

        # walk upwards
        data = Row(index='path',
                  operator='_relativePath',
                  values='../../')
        parsed = queryparser._relativePath(context, data)
        expected = {'path': {'query': '/%s' % MOCK_SITE_ID}}
        self.assertEqual(parsed, expected)

        # if you walk beyond INavigatinRoot it should stop and return
        data = Row(index='path',
                  operator='_relativePath',
                  values='../../../')
        parsed = queryparser._relativePath(context, data)
        expected = {'path': {'query': '/%s' % MOCK_SITE_ID}}
        self.assertEqual(parsed, expected)

        # reach a subfolder on Plone root
        data = Row(index='path',
                   operator='_relativePath',
                   values='../../ham')
        parsed = queryparser._relativePath(context, data)
        expected = {'path': {'query': '/%s/ham' % MOCK_SITE_ID}}
        self.assertEqual(parsed, expected)

        # reach a subfolder on parent of collection
        data = Row(index='path',
                   operator='_relativePath',
                   values='../egg')
        parsed = queryparser._relativePath(context, data)
        expected = {'path': {'query': '/%s/bar/egg' % MOCK_SITE_ID}}
        self.assertEqual(parsed, expected)

    def test_getPathByUID(self):
        actual = queryparser.getPathByUID(MockSite(), '00000000000000001')
        self.assertEqual(actual, ['', 'site', 'foo'])
