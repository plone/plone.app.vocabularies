# KEPT HERE FOR BBB UNTIL PLONE 6
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.browser.interfaces import ITerms
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource
from zope.schema.vocabulary import SimpleTerm

import warnings


try:
    from zope.formlib.interfaces import ISourceQueryView
except ImportError:
    from zope.interface import Interface

    class ISourceQueryView(Interface):
        pass


@implementer(ISource)
@provider(IContextSourceBinder)
class GroupsSource:
    """
    >>> from plone.app.vocabularies.tests.base import create_context
    >>> from plone.app.vocabularies.tests.base import DummyTool

    >>> context = create_context()

    >>> tool = DummyTool('acl_users')
    >>> groups = ('group1', 'group2')
    >>> def getGroupById(value, default):
    ...     return value in groups and value or default
    >>> tool.getGroupById = getGroupById
    >>> def searchGroups(name=None):
    ...     return [dict(groupid=u) for u in groups]
    >>> tool.searchGroups = searchGroups
    >>> context.acl_users = tool

    >>> source = GroupsSource(context)
    >>> source
    <plone.app.vocabularies.groups.GroupsSource object at ...>

    >>> len(source.search(''))
    2

    >>> len(source.search(u'\xa4'))
    2

    >>> 'group1' in source, 'noone' in source
    (True, False)

    >>> source.get('group1'), source.get('noone')
    ('group1', None)
    """

    def __init__(self, context):
        msg = "GroupsSource is deprecated and will be removed on " "Plone 6"
        warnings.warn(msg, DeprecationWarning)
        self.context = context
        self.users = getToolByName(context, "acl_users")

    def __contains__(self, value):
        """Return whether the value is available in this source"""
        if self.get(value) is None:
            return False
        return True

    def search(self, query):
        # XXX: For some reason, this doesn't seem to know how to match on
        # title, only name, and seems to match other random groups if
        # it's unicode

        try:
            name = query.encode("ascii")
        except UnicodeEncodeError:
            name = query

        return [u["groupid"] for u in self.users.searchGroups(name=name)]

    def get(self, value):
        return self.users.getGroupById(value, None)


@implementer(ITerms, ISourceQueryView)
class GroupsSourceQueryView:
    """
    >>> from plone.app.vocabularies.tests.base import create_context
    >>> from plone.app.vocabularies.tests.base import DummyTool
    >>> from plone.app.vocabularies.tests.base import Request

    >>> context = create_context()

    >>> class Group(object):
    ...     def __init__(self, id):
    ...         self.id = id
    ...
    ...     def getProperty(self, value, default):
    ...         return self.id
    ...
    ...     getId = getProperty

    >>> tool = DummyTool('acl_users')
    >>> groups = ('group1', 'group2')
    >>> def getGroupById(value, default):
    ...     return value in groups and Group(value) or None
    >>> tool.getGroupById = getGroupById
    >>> def searchGroups(name=None):
    ...     return [dict(groupid=u) for u in groups]
    >>> tool.searchGroups = searchGroups
    >>> context.acl_users = tool

    >>> source = GroupsSource(context)
    >>> source
    <plone.app.vocabularies.groups.GroupsSource object at ...>

    >>> view = GroupsSourceQueryView(source, Request())
    >>> view
    <plone.app.vocabularies.groups.GroupsSourceQueryView object at ...>

    >>> view.getTerm('group1')
    <zope.schema.vocabulary.SimpleTerm object at ...>

    >>> view.getValue('group1')
    'group1'

    >>> view.getValue('noone')
    Traceback (most recent call last):
    ...
    LookupError: noone

    >>> template = view.render(name='t')

    >>> u'<input type="text" name="t.query" value="" />' in template
    True

    >>> u'<input type="submit" name="t.search" value="Search" />' in template
    True

    >>> request = Request(form={'t.search' : True, 't.query' : 'value'})
    >>> view = GroupsSourceQueryView(source, request)
    >>> view.results('t')
    ['group1', 'group2']
    """

    template = ViewPageTemplateFile("searchabletextsource.pt")

    def __init__(self, context, request):
        msg = "GroupsSourceQueryView is deprecated and will be removed on " "Plone 6"
        warnings.warn(msg, DeprecationWarning)
        self.context = context
        self.request = request

    def getTerm(self, value):
        group = self.context.get(value)
        token = value
        title = value
        if group is not None:
            title = group.getProperty("title", None) or group.getId()
        return SimpleTerm(value, token=token, title=title)

    def getValue(self, token):
        if token not in self.context:
            raise LookupError(token)
        return token

    def render(self, name):
        return self.template(name=name)

    def results(self, name):
        # check whether the normal search button was pressed
        if name + ".search" in self.request.form:
            query_fieldname = name + ".query"
            if query_fieldname in self.request.form:
                query = self.request.form[query_fieldname]
                if query != "":
                    return self.context.search(query)
