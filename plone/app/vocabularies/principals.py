from plone.app.vocabularies import SlicableVocabulary
from plone.app.vocabularies.groups import GroupsSource
from plone.app.vocabularies.security import GroupsVocabularyFactory
from plone.app.vocabularies.users import _createUserTerm
from plone.app.vocabularies.users import UsersFactory
from plone.app.vocabularies.users import UsersSource
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm


@implementer(ISource)
@provider(IContextSourceBinder)
class PrincipalsSource(object):
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
      >>> groups = ('group1', 'group2')
      >>> def getGroupById(value, default):
      ...     return value in groups and value or default
      >>> tool.getGroupById = getGroupById
      >>> def searchGroups(name=None):
      ...     return [dict(groupid=u) for u in groups]
      >>> tool.searchGroups = searchGroups
      >>> context.acl_users = tool

      >>> source = PrincipalsSource(context)
      >>> source
      <plone.app.vocabularies.principals.PrincipalsSource object at ...>

      >>> len(source.search(None))
      4

      >>> 'user:user1' in source, 'user:noone' in source
      (True, False)

      >>> 'group:group1' in source, 'group:noone' in source
      (True, False)

      >>> source.get('user:user1'), source.get('user:noone')
      ('user1', None)

     >>> source.get('group:group1'), source.get('group:noone')
     ('group1', None)
    """

    def __init__(self, context):
        self.context = context
        self.users_source = UsersSource(context)
        self.groups_source = GroupsSource(context)

    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if self.get(value) is None:
            return False
        return True

    def search(self, query):
        results = self.users_source.search(query)
        results.extend(self.groups_source.search(query))
        return results

    def get(self, value):
        if not value:
            return
        if value.startswith('user:'):
            value = value.replace('user:', '')
            return self.users_source.get(value)
        else:
            value = value.replace('group:', '')
            return self.groups_source.get(value)


def _createGroupTerm(groupid, context=None, acl_users=None):
    if acl_users is None:
        acl_users = getToolByName(context, 'acl_users')
    group = acl_users.getGroupById(groupid, None)
    groupname = groupid
    if group:
        groupname = group.getProperty('name', None) or groupname
    token = groupid.encode('unicode_escape') if isinstance(
        groupid, unicode) else groupid
    return SimpleTerm(groupid, token, groupname)


class PrincipalsVocabulary(SlicableVocabulary):

    def __init__(self, terms, context, *interfaces):
        super(PrincipalsVocabulary, self).__init__(terms, *interfaces)
        self._users = getToolByName(getSite(), 'acl_users')

    def __contains__(self, value):
        if value.startswith('user:'):
            if self._users.getUserById(value.replace('user:', ''), None):
                return True
        else:
            if self._users.getGroupById(value.replace('group:', ''), None):
                return True
        return False

    def prefix_term(self, term, prefix):
        term.token = prefix + term.token
        term.value = prefix + term.value
        return term

    def getTerm(self, _id):
        if _id.startswith('user:'):
            return self.prefix_term(
                _createUserTerm(_id.replace('user:', ''), acl_users=self._users),
                'user:')
        else:
            return self.prefix_term(
                _createGroupTerm(_id.replace('group:', ''), acl_users=self._users),
                'group:')
    getTermByToken = getTerm

    def __iter__(self):
        return self._terms


@implementer(IVocabularyFactory)
class PrincipalsFactory(object):
    """Factory creating a UsersVocabulary
    """

    def prefix_values(self, terms, prefix):
        result = []
        for term in terms:
            term.token = prefix + term.token
            term.value = prefix + term.value
            result.append(term)
        return result

    def filter(self, term):
        """
        ability to override to provide custom filtering
        """
        return True

    def lazy_filtered_list(self, *lists):
        for ll in lists:
            for item in ll:
                if self.filter(item):
                    yield item

    def __call__(self, context, query=''):
        """
        we're simply combining the user and groups results
        """
        users = UsersFactory()(context, query)
        groups = GroupsVocabularyFactory(context, query)
        return PrincipalsVocabulary(self.lazy_filtered_list(
            self.prefix_values(users._terms, 'user:') +
            self.prefix_values(groups._terms, 'group:')), context)
