# -*- coding: utf-8 -*-
from plone.app.vocabularies import SlicableVocabulary
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.browser.interfaces import ITerms
from zope.component.hooks import getSite
from zope.formlib.interfaces import ISourceQueryView
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm


def _createUserTerm(userid, context=None, acl_users=None):
    if acl_users is None:
        acl_users = getToolByName(context, "acl_users")
    user = acl_users.getUserById(userid, None)
    fullname = userid
    if user:
        fullname = user.getProperty('fullname', None) or userid
    token = userid.encode('unicode_escape') if isinstance(userid, unicode) else userid
    return SimpleTerm(userid, token, fullname)


@implementer(ISource)
@provider(IContextSourceBinder)
class UsersSource(object):
    """
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> context = create_context()

      >>> tool = DummyTool('acl_users')
      >>> users = ('user1', 'user2')
      >>> def getUserById(value, default):
      ...     return value in users and value or default
      >>> tool.getUserById = getUserById
      >>> def searchUsers(fullname=None):
      ...     return [dict(userid=u) for u in users]
      >>> tool.searchUsers = searchUsers
      >>> context.acl_users = tool

      >>> source = UsersSource(context)
      >>> source
      <plone.app.vocabularies.users.UsersSource object at ...>

      >>> len(source.search(None))
      2

      >>> 'user1' in source, 'noone' in source
      (True, False)

      >>> source.get('user1'), source.get('noone')
      ('user1', None)
    """

    def __init__(self, context):
        self.context = context
        self.users = getToolByName(context, "acl_users")

    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if self.get(value) is None:
            return False
        return True

    def search(self, query):
        return [u['userid'] for u in self.users.searchUsers(fullname=query)]

    def get(self, value):
        return self.users.getUserById(value, None)


class UsersVocabulary(SlicableVocabulary):

    def __init__(self, terms, context, *interfaces):
        super(UsersVocabulary, self).__init__(terms, *interfaces)
        self._users = getToolByName(context, "acl_users")

    @classmethod
    def fromItems(cls, items, context, *interfaces):
        def lazy(items):
            for item in items:
                yield cls.createTerm(item['userid'], context)
        return cls(lazy(items), context, *interfaces)
    fromValues = fromItems

    @classmethod
    def createTerm(cls, userid, context):
        return _createUserTerm(userid, context=context)

    def __contains__(self, value):
        return self._users.getUserById(value, None) and True or False

    def getTerm(self, userid):
        return _createUserTerm(userid, acl_users=self._users)
    getTermByToken = getTerm

    def __iter__(self):
        return self._terms


@implementer(IVocabularyFactory)
class UsersFactory(object):
    """Factory creating a UsersVocabulary
    """

    def __call__(self, context, query=''):
        if context is None:
            context = getSite()
        users = getToolByName(context, "acl_users")
        return UsersVocabulary.fromItems(
            users.searchUsers(fullname=query),
            context
        )


@implementer(ITerms, ISourceQueryView)
class UsersSourceQueryView(object):
    """
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool
      >>> from plone.app.vocabularies.tests.base import Request

      >>> context = create_context()

      >>> class User(object):
      ...     def __init__(self, id):
      ...         self.id = id
      ...
      ...     def getProperty(self, value, default):
      ...         return self.id
      ...
      ...     getId = getProperty

      >>> tool = DummyTool('acl_users')
      >>> users = ('user1', 'user2')
      >>> def getUserById(value, default):
      ...     return value in users and User(value) or None
      >>> tool.getUserById = getUserById
      >>> def searchUsers(fullname=None):
      ...     return [dict(userid=u) for u in users]
      >>> tool.searchUsers = searchUsers
      >>> context.acl_users = tool

      >>> source = UsersSource(context)
      >>> source
      <plone.app.vocabularies.users.UsersSource object at ...>

      >>> view = UsersSourceQueryView(source, Request())
      >>> view
      <plone.app.vocabularies.users.UsersSourceQueryView object at ...>

      >>> view.getTerm('user1')
      <zope.schema.vocabulary.SimpleTerm object at ...>

      >>> view.getValue('user1')
      'user1'

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
      >>> view = UsersSourceQueryView(source, request)
      >>> view.results('t')
      ['user1', 'user2']
    """

    template = ViewPageTemplateFile('searchabletextsource.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getTerm(self, value):
        user_id = value
        return _createUserTerm(user_id, context=self.context.context)

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
                if query != '':
                    return self.context.search(query)
