# -*- coding: utf-8 -*-
from plone.app.vocabularies import SlicableVocabulary
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm

import six


def _createGroupTerm(groupid, context=None, acl_users=None):
    if acl_users is None:
        acl_users = getToolByName(context, 'acl_users')
    user = acl_users.getGroupById(groupid, None)
    title = groupid
    if user:
        title = user.getProperty('title', None) or groupid
    token = groupid.encode('unicode_escape') if isinstance(
        groupid, six.text_type) else groupid
    return SimpleTerm(groupid, token, title)


class GroupsVocabulary(SlicableVocabulary):

    def __init__(self, terms, context, *interfaces):
        super(GroupsVocabulary, self).__init__(terms, *interfaces)
        self._acl_users = getToolByName(context, 'acl_users')

    @classmethod
    def fromItems(cls, items, context, *interfaces):
        def lazy(items):
            for item in items:
                yield cls.createTerm(item['groupid'], context)
        return cls(lazy(items), context, *interfaces)
    fromValues = fromItems

    @classmethod
    def createTerm(cls, groupid, context):
        return _createGroupTerm(groupid, context=context)

    def __contains__(self, value):
        return bool(self._acl_users.getGroupById(value, None))

    def getTerm(self, groupid):
        return _createGroupTerm(groupid, acl_users=self._acl_users)

    getTermByToken = getTerm

    def __iter__(self):
        return self._terms


@implementer(IVocabularyFactory)
class GroupsFactory(object):
    """Factory creating a GroupsVocabulary

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
    >>> def searchGroups(title=None):
    ...     return [dict(groupid=u) for u in groups if title in u]
    >>> tool.searchGroups = searchGroups
    >>> context.acl_users = tool
    >>> factory = GroupsFactory()

    When the registry record 'plone.many_groups' is set to True
    no group is returned to avoid expensive queries if no query filter is passed
    >>> def patched_getUtility(arg):
    ...     return {'plone.many_groups': True}
    >>> backup = getUtility.__code__
    >>> getUtility.__code__ = patched_getUtility.__code__
    >>> [x.title for x in factory(context, '')]
    []
    >>> getUtility.__code__ = backup

    Passing a non empty query string will work ignore the 'plone.many_groups'
    setting
    >>> [x.title for x in factory(context, '1')]
    ['group1']
    """
    def should_search(self, query):
        ''' Test if we should search for groups
        '''
        if query:
            return True
        registry = getUtility(IRegistry)
        return not registry.get('plone.many_groups')

    def __call__(self, context, query=''):
        if context is None:
            context = getSite()
        if self.should_search(query):
            acl_users = getToolByName(context, 'acl_users')
            # name is passed and expected, but also searched as title
            groups = acl_users.searchGroups(name=query)
        else:
            groups = []
        return GroupsVocabulary.fromItems(groups, context)
