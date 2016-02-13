# -*- coding: utf-8 -*-
from Acquisition import aq_get
from operator import attrgetter
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite

PMF = MessageFactory('plone')


@implementer(IVocabularyFactory)
class RolesVocabulary(object):
    """Vocabulary factory for roles in the portal

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.Roles'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> len(util(context))
      0

      >>> tool = DummyTool('portal_membership')
      >>> def getPortalRoles():
      ...    return ('Anonymous', 'Authenticated', 'Manager', 'Ploonies')
      >>> tool.getPortalRoles = getPortalRoles
      >>> context.portal_membership = tool

      >>> roles = util(context)
      >>> roles
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(roles.by_token)
      4

      >>> manager = roles.by_token['Manager']
      >>> manager.title, manager.token, manager.value
      (u'Manager', 'Manager', 'Manager')
    """

    def __call__(self, context):
        site = getSite()
        mtool = getToolByName(site, 'portal_membership', None)
        if mtool is None:
            return SimpleVocabulary([])

        items = []
        request = aq_get(mtool, 'REQUEST', None)
        roles = mtool.getPortalRoles()
        for role_id in roles:
            role_title = translate(PMF(role_id), context=request)
            items.append(SimpleTerm(role_id, role_id, role_title))

        missing_roles = ["Anonymous", "Authenticated"]
        for role_id in missing_roles:
            if role_id in roles:
                continue
            role_title = translate(PMF(role_id), context=request)
            items.append(SimpleTerm(role_id, role_id, role_title))
        items.sort(key=attrgetter('title'))

        return SimpleVocabulary(items)

RolesVocabularyFactory = RolesVocabulary()


@implementer(IVocabularyFactory)
class GroupsVocabulary(object):
    """Vocabulary factory for groups in the portal

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.Groups'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> len(util(context))
      0

      >>> class DummyGroup(object):
      ...     def __init__(self, id, name):
      ...         self.id = id
      ...         self.name = name
      ...
      ...     def getGroupId(self):
      ...         return self.id
      ...
      ...     def getGroupTitleOrName(self):
      ...         return self.name

      >>> tool = DummyTool('portal_groups')
      >>> def listGroups():
      ...     return (DummyGroup('editors', 'Editors'),
      ...             DummyGroup('viewers', 'Viewers'))
      >>> tool.listGroups = listGroups
      >>> context.portal_groups = tool

      >>> groups = util(context)
      >>> groups
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(groups.by_token)
      2

      >>> editors = groups.by_token['editors']
      >>> editors.title, editors.token, editors.value
      ('Editors', 'editors', 'editors')
    """

    def __call__(self, context):
        items = []
        site = getSite()
        gtool = getToolByName(site, 'portal_groups', None)
        if gtool is not None:
            groups = gtool.listGroups()
            items = [(g.getGroupId(), g.getGroupTitleOrName()) for g in groups]
            items.sort()
            items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)

GroupsVocabularyFactory = GroupsVocabulary()


@implementer(IVocabularyFactory)
class PermissionsVocabulary(object):
    """Vocabulary factory for permissions.
    """

    def __call__(self, context):
        site = getSite()
        items = [SimpleTerm(perm, perm, perm)
            for perm in site.possible_permissions()]
        return SimpleVocabulary(items)

PermissionsVocabularyFactory = PermissionsVocabulary()
