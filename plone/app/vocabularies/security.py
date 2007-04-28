from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName

class RolesVocabulary(object):
    """Vocabulary factory for roles in the portal
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        mtool = getToolByName(context, 'portal_membership')
        items = [ (r, r) for r in mtool.getPortalRoles() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)

RolesVocabularyFactory = RolesVocabulary()

class GroupsVocabulary(object):
    """Vocabulary factory for groups in the portal
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        mtool = getToolByName(context, 'portal_groups')
        items = [ (g.getGroupId(), g.getGroupName()) for g in mtool.listGroups() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)
        
GroupsVocabularyFactory = GroupsVocabulary()
