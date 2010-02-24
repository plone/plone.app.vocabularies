from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite

from Products.Archetypes.mimetype_utils import getAllowableContentTypes
from Products.Archetypes.mimetype_utils import getAllowedContentTypes
from Products.CMFCore.utils import getToolByName


class AllowableContentTypesVocabulary(object):
    """Vocabulary factory for allowable content types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.AllowableContentTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> tool = DummyTool('portal_transforms')
      >>> def listAvailableTextInputs():
      ...     return ('text/plain', 'text/spam')
      >>> tool.listAvailableTextInputs = listAvailableTextInputs
      >>> context.portal_transforms = tool

      >>> types = util(context)
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
        site = getSite()
        items = list(getAllowableContentTypes(site))
        items.sort()
        items = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(items)

AllowableContentTypesVocabularyFactory = AllowableContentTypesVocabulary()


class AllowedContentTypesVocabulary(object):
    """Vocabulary factory for allowed content types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.AllowedContentTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> tool = DummyTool('portal_transforms')
      >>> def listAvailableTextInputs():
      ...     return ('text/plain', 'text/spam')
      >>> tool.listAvailableTextInputs = listAvailableTextInputs
      >>> context.portal_transforms = tool

      >>> tool = DummyTool('portal_properties')
      >>> class DummyProperties(object):
      ...     def hasProperty(self, value):
      ...         return True
      ...
      ...     def getProperty(self, value):
      ...         return ('text/spam', )
      >>> tool.site_properties = DummyProperties()
      >>> context.portal_properties = tool

      >>> types = util(context)
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
        site = getSite()
        items = list(getAllowedContentTypes(site))
        items.sort()
        items = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(items)

AllowedContentTypesVocabularyFactory = AllowedContentTypesVocabulary()


class PortalTypesVocabulary(object):
    """Vocabulary factory for portal types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTypeTool

      >>> name = 'plone.app.vocabularies.PortalTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> context.portal_types = DummyTypeTool()
      >>> types = util(context)
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
        site = getSite()
        ttool = getToolByName(site, 'portal_types', None)
        if ttool is None:
            return SimpleVocabulary([])
        items = [(ttool[t].Title(), t)
                 for t in ttool.listContentTypes()]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

PortalTypesVocabularyFactory = PortalTypesVocabulary()


class UserFriendlyTypesVocabulary(object):
    """Vocabulary factory for user friendly portal types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool
      >>> from plone.app.vocabularies.tests.base import DummyTypeTool

      >>> name = 'plone.app.vocabularies.UserFriendlyTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> context.portal_types = DummyTypeTool()
      >>> tool = DummyTool('plone_utils')
      >>> def getUserFriendlyTypes():
      ...     return ('Document', )
      >>> tool.getUserFriendlyTypes = getUserFriendlyTypes
      >>> context.plone_utils = tool

      >>> types = util(context)
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
        site = getSite()
        ptool = getToolByName(site, 'plone_utils', None)
        ttool = getToolByName(site, 'portal_types', None)
        if ptool is None or ttool is None:
            return SimpleVocabulary([])
        items = [(ttool[t].Title(), t)
                 for t in ptool.getUserFriendlyTypes()]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

UserFriendlyTypesVocabularyFactory = UserFriendlyTypesVocabulary()


BAD_TYPES = ("ATBooleanCriterion", "ATDateCriteria", "ATDateRangeCriterion",
             "ATListCriterion", "ATPortalTypeCriterion", "ATReferenceCriterion",
             "ATSelectionCriterion", "ATSimpleIntCriterion", "Plone Site",
             "ATSimpleStringCriterion", "ATSortCriterion",
             "Discussion Item", "TempFolder", "ATCurrentAuthorCriterion",
             "ATPathCriterion", "ATRelativePathCriterion", )


class ReallyUserFriendlyTypesVocabulary(object):
    """Vocabulary factory for really user friendly portal types.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyType
      >>> from plone.app.vocabularies.tests.base import DummyTypeTool

      >>> name = 'plone.app.vocabularies.ReallyUserFriendlyTypes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> tool = DummyTypeTool()
      >>> tool['ATBooleanCriterion'] = DummyType('Boolean Criterion')
      >>> context.portal_types = tool

      >>> types = util(context)
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
        site = getSite()
        ttool = getToolByName(site, 'portal_types', None)
        if ttool is None:
            return SimpleVocabulary([])
        items = [SimpleTerm(t, t, ttool[t].Title())
                 for t in ttool.listContentTypes()
                 if t not in BAD_TYPES]
        return SimpleVocabulary(items)

ReallyUserFriendlyTypesVocabularyFactory = ReallyUserFriendlyTypesVocabulary()
