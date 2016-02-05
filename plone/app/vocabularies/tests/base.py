# -*- coding: utf-8 -*-
from Products.ZCTextIndex.ParseTree import ParseError
from plone.app.layout.navigation.interfaces import INavigationRoot
from OFS.interfaces import IItem
from zope.interface import implements
from zope.site.hooks import setSite


def create_context():
    context = DummyContext()
    setSite(context)
    return context


class DummyContext(object):

    def __init__(self):
        self.__name__ = 'dummy'
        self.__parent__ = None

    def getSiteManager(self):
        return self

    def queryUtility(self, iface, name='', default=None):
        """Query for a utility.

        Note that earlier zope.component versions had 'provided'
        instead of 'iface', but that should not matter.
        """
        return default

    def getPhysicalPath(self):
        return ['', self.__name__]

    def absolute_url(self, relative=False):
        return '/'.join(self.getPhysicalPath())



class DummyUrlTool(object):

    name = 'portal_url'

    def __init__(self, context):
        self.portal = context

    def __call__(self):
        return self.portal.__name__

    def getPortalObject(self):
        return self.portal


class DummyTool(object):

    def __init__(self, name):
        self.name = name


class DummyType(object):

    def __init__(self, title):
        self.title = title

    def Title(self):
        return self.title


class DummyTypeTool(dict):

    def __init__(self):
        self['Document'] = DummyType('Page')
        self['Event'] = DummyType('Event')

    def listContentTypes(self):
        return self.keys()


class Response(dict):

    def getHeader(self, value):
        return 'header %s' % value


class Request(dict):

    debug = False
    response = Response()

    def __init__(self, form=None):
        self.form = form


class Brain(object):

    Title = 'BrainTitle'
    is_folderish = True

    def __init__(self, rid):
        self.rid = rid

    def getPath(self):
        return self.rid

    @property
    def UID(self):
        return self.rid


class DummyCatalog(dict):
    implements(IItem)

    def __init__(self, values):
        self.indexes = {}
        for r in values:
            self[r] = Brain(r)

    def __call__(self, **values):
        if 'SearchableText' in values:
            st = values['SearchableText']
            if st.startswith('error'):
                raise ParseError
        return self.values()

    @property
    def _catalog(self):
        return self

    def getrid(self, value):
        return value in self and value or None

    def getIndex(self, name):
        return self.indexes[name]


class DummyContent(object):
    def __init__(self, title, subjects=[]):
        self.title = title
        self.subjects = subjects

    def Title(self):
        return self.title

    def Subject(self):
        return self.subjects


class DummyNavRoot(object):
    implements(INavigationRoot)
    __parent__ = None

    def __init__(self, _id, title=None, parent=None):
        self.__name__ = _id
        self.title = title or _id
        if parent:
            self.__parent__ = parent

    def getPhysicalPath(self):
        return ['', self.__parent__.__name__, self.__name__]

    def absolute_url(self, relative=False):
        return '/'.join(self.getPhysicalPath())

    @property
    def portal_catalog(self):
        # fake tool acquisition
        return self.__parent__.portal_catalog

    @property
    def portal_url(self):
        # fake tool acquisition
        return self.__parent__.portal_url
