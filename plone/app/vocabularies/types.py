from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.Archetypes.mimetype_utils import getAllowableContentTypes
from Products.Archetypes.mimetype_utils import getAllowedContentTypes

from Products.CMFCore.utils import getToolByName


class AllowableContentTypesVocabulary(object):
    """Vocabulary factory for allowable content types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.AllowableContentTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> tool = DummyTool('portal_transforms')
      >>> def listAvailableTextInputs():
      ...     return ('text/plain', 'text/spam')
      >>> tool.listAvailableTextInputs = listAvailableTextInputs
      >>> context2.portal_transforms = tool

      >>> types = util(context1)
      >>> types
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(types.by_token)
      2

      >>> doc = types.by_token['text/plain']
      >>> doc.title, doc.token, doc.value
      ('text/plain', 'text/plain', 'text/plain')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        items = list(getAllowableContentTypes(context))
        items.sort()
        items = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(items)

AllowableContentTypesVocabularyFactory = AllowableContentTypesVocabulary()


class AllowedContentTypesVocabulary(object):
    """Vocabulary factory for allowed content types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.AllowedContentTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> tool = DummyTool('portal_transforms')
      >>> def listAvailableTextInputs():
      ...     return ('text/plain', 'text/spam')
      >>> tool.listAvailableTextInputs = listAvailableTextInputs
      >>> context2.portal_transforms = tool

      >>> tool = DummyTool('portal_properties')
      >>> class DummyProperties(object):
      ...     def hasProperty(self, value):
      ...         return True
      ...
      ...     def getProperty(self, value):
      ...         return ('text/spam', )
      >>> tool.site_properties = DummyProperties()
      >>> context2.portal_properties = tool

      >>> types = util(context1)
      >>> types
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(types.by_token)
      1

      >>> doc = types.by_token['text/plain']
      >>> doc.title, doc.token, doc.value
      ('text/plain', 'text/plain', 'text/plain')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        items = list(getAllowedContentTypes(context))
        items.sort()
        items = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(items)

AllowedContentTypesVocabularyFactory = AllowedContentTypesVocabulary()


class PortalTypesVocabulary(object):
    """Vocabulary factory for portal types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTypeTool

      >>> name = 'plone.app.vocabularies.PortalTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> context2.portal_types = DummyTypeTool()

      >>> types = util(context1)
      >>> types
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(types.by_token)
      2

      >>> doc = types.by_token['Document']
      >>> doc.title, doc.token, doc.value
      ('Page', 'Document', 'Document')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ttool = getToolByName(context, 'portal_types', None)
        if ttool is None:
            return None
        items = [(ttool[t].Title(), t)
                 for t in ttool.listContentTypes()]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

PortalTypesVocabularyFactory = PortalTypesVocabulary()


class UserFriendlyTypesVocabulary(object):
    """Vocabulary factory for user friendly portal types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool
      >>> from plone.app.vocabularies.tests.base import DummyTypeTool

      >>> name = 'plone.app.vocabularies.UserFriendlyTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> context2.portal_types = DummyTypeTool()
      >>> tool = DummyTool('plone_utils')
      >>> def getUserFriendlyTypes():
      ...     return ('Document', )
      >>> tool.getUserFriendlyTypes = getUserFriendlyTypes
      >>> context2.plone_utils = tool

      >>> types = util(context1)
      >>> types
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(types.by_token)
      1

      >>> doc = types.by_token['Document']
      >>> doc.title, doc.token, doc.value
      ('Page', 'Document', 'Document')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ptool = getToolByName(context, 'plone_utils', None)
        ttool = getToolByName(context, 'portal_types', None)
        if ptool is None or ttool is None:
            return None
        items = [(ttool[t].Title(), t)
                 for t in ptool.getUserFriendlyTypes()]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

UserFriendlyTypesVocabularyFactory = UserFriendlyTypesVocabulary()


BAD_TYPES = ("ATBooleanCriterion", "ATDateCriteria", "ATDateRangeCriterion",
             "ATListCriterion", "ATPortalTypeCriterion", "ATReferenceCriterion",
             "ATSelectionCriterion", "ATSimpleIntCriterion", "Plone Site",
             "ATSimpleStringCriterion", "ATSortCriterion", "ChangeSet",
             "Discussion Item", "TempFolder", "ATCurrentAuthorCriterion",
             "ATPathCriterion", "ATRelativePathCriterion", )


class ReallyUserFriendlyTypesVocabulary(object):
    """Vocabulary factory for really user friendly portal types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyType
      >>> from plone.app.vocabularies.tests.base import DummyTypeTool

      >>> name = 'plone.app.vocabularies.ReallyUserFriendlyTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> tool = DummyTypeTool()
      >>> tool['ATBooleanCriterion'] = DummyType('Boolean Criterion')
      >>> context2.portal_types = tool

      >>> types = util(context1)
      >>> types
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(types.by_token)
      2

      >>> doc = types.by_token['Document']
      >>> doc.title, doc.token, doc.value
      ('Page', 'Document', 'Document')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ttool = getToolByName(context, 'portal_types', None)
        if ttool is None:
            return None
        items = [SimpleTerm(t, t, ttool[t].Title())
                 for t in ttool.listContentTypes()
                 if t not in BAD_TYPES]
        return SimpleVocabulary(items)

ReallyUserFriendlyTypesVocabularyFactory = ReallyUserFriendlyTypesVocabulary()
