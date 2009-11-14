from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName

class RolesVocabulary(object):
    """Vocabulary factory for roles in the portal

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.Roles'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> tool = DummyTool('portal_membership')
      >>> def getPortalRoles():
      ...     return ('Anonymous', 'Manager', 'Ploonies')
      >>> tool.getPortalRoles = getPortalRoles
      >>> context2.portal_membership = tool

      >>> roles = util(context1)
      >>> roles
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(roles.by_token)
      3

      >>> manager = roles.by_token['Manager']
      >>> manager.title, manager.token, manager.value
      ('Manager', 'Manager', 'Manager')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        mtool = getToolByName(context, 'portal_membership', None)
        if mtool is None:
            return None
        items = list(mtool.getPortalRoles())
        items.sort()
        items = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(items)

RolesVocabularyFactory = RolesVocabulary()

class GroupsVocabulary(object):
    """Vocabulary factory for groups in the portal

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.Groups'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> class DummyGroup(object):
      ...     def __init__(self, id, name):
      ...         self.id = id
      ...         self.name = name
      ...
      ...     def getGroupId(self):
      ...         return self.id
      ...
      ...     def getGroupName(self):
      ...         return self.name

      >>> tool = DummyTool('portal_groups')
      >>> def listGroups():
      ...     return (DummyGroup('editors', 'Editors'),
      ...             DummyGroup('viewers', 'Viewers'))
      >>> tool.listGroups = listGroups
      >>> context2.portal_groups = tool

      >>> groups = util(context1)
      >>> groups
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(groups.by_token)
      2

      >>> editors = groups.by_token['editors']
      >>> editors.title, editors.token, editors.value
      ('Editors', 'editors', 'editors')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        gtool = getToolByName(context, 'portal_groups', None)
        if gtool is None:
            return None
        items = [ (g.getGroupId(), g.getGroupName()) for g in gtool.listGroups() ]
        items.sort()
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)
        
GroupsVocabularyFactory = GroupsVocabulary()
