# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class ActionCategoriesVocabulary(object):
    """Provides an actions categories vocabulary"""

    def __call__(self, context):
        portal_actions = getToolByName(context, 'portal_actions')

        # Building the list of action categories
        try:
            categories = portal_actions.listFilteredActionsFor(context).keys()
        except:
            portal = context.portal_url.getPortalObject()
            categories = portal.portal_actions.objectIds()
        categories.sort()
        return SimpleVocabulary(
            [SimpleTerm(cat, title=cat) for cat in categories]
        )


ActionCategoriesVocabularyFactory = ActionCategoriesVocabulary()


@implementer(IVocabularyFactory)
class PortalActionCategoriesVocabulary(object):
    """Provides portal action categories vocabulary."""

    def __call__(self, context):
        portal_actions = getToolByName(context, 'portal_actions')
        categories = portal_actions.objectIds()
        categories.sort()
        terms = []
        for category in categories:
            if category == 'controlpanel':
                continue
            title = portal_actions.get(category).title
            if title:
                title = _(title)
            else:
                title = category
            terms.append(SimpleTerm(category, title=title))
        return SimpleVocabulary(terms)

PortalActionCategoriesVocabularyFactory = PortalActionCategoriesVocabulary()
