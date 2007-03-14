from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.interfaces import IMembershipTool
from Products.PlonePAS.interfaces.group import IGroupTool


class RolesVocabulary(object):
    """Vocabulary factory for roles in the portal
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        mtool = getUtility(IMembershipTool)
        items = [ (r, r) for r in mtool.getPortalRoles() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)

RolesVocabularyFactory = RolesVocabulary()


class GroupsVocabulary(object):
    """Vocabulary factory for groups in the portal
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        mtool = getUtility(IGroupTool)
        items = [ (g.getGroupId(), g.getGroupName()) for g in mtool.listGroups() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)
        
GroupsVocabularyFactory = GroupsVocabulary()
