from Acquisition import aq_get
from operator import attrgetter
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import zope.deferredimport


zope.deferredimport.deprecated(
    "Import from plone.app.vocabularies.principals instead",
    GroupsFactory="plone.app.vocabularies:principals.GroupsFactory",
    GroupsVocabulary="plone.app.vocabularies:principals.GroupsVocabulary",
)

PMF = MessageFactory("plone")


@implementer(IVocabularyFactory)
class RolesVocabulary:
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
        mtool = getToolByName(site, "portal_membership", None)
        if mtool is None:
            return SimpleVocabulary([])

        items = []
        request = aq_get(mtool, "REQUEST", None)
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
        items.sort(key=attrgetter("title"))

        return SimpleVocabulary(items)


RolesVocabularyFactory = RolesVocabulary()


@implementer(IVocabularyFactory)
class PermissionsVocabulary:
    """Vocabulary factory for permissions."""

    def __call__(self, context):
        site = getSite()
        items = [SimpleTerm(perm, perm, perm) for perm in site.possible_permissions()]
        return SimpleVocabulary(items)


PermissionsVocabularyFactory = PermissionsVocabulary()
