from Acquisition import aq_get
from plone.app.vocabularies import PermissiveVocabulary
from Products.CMFCore.utils import getToolByName
from unidecode import unidecode
from zope.component.hooks import getSite
from zope.deprecation import deprecate
from zope.i18n import translate
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def getAllowedContentTypes(context):
    """computes the list of allowed content types ...
    Here the mime types allowed in text fields are meant.

    It does so by subtracting the site property blacklist from the list of
    allowable (overall available) types.
    """
    allowable_types = getAllowableContentTypes(context)
    # By default the next one is empty, but theoretically someone overwrites it.
    forbidden_types = getForbiddenContentTypes(context)
    allowed_types = [ctype for ctype in allowable_types if ctype not in forbidden_types]
    return allowed_types


def getAllowableContentTypes(context):
    """retrieves the list of available content types (aka mime-types) ...

    ... by querying portal transforms.

    Cite from over there:
    This returns a list of mimetypes that can be used as input for textfields
    by building a list of the inputs beginning with "text/" of all
    transforms.
    """
    portal_transforms = getToolByName(context, "portal_transforms")
    return portal_transforms.listAvailableTextInputs()


@deprecate("Returns nothing by default. Will be removed in Plone 7.")
def getForbiddenContentTypes(context):
    """Get forbidden contenttypes.

    This is a list of mime-types not allowed in text input fields.

    We used to get this from
    portal_properties.site_properties.forbidden_contenttypes
    Maybe we should have moved this to portal_registry, but no-one did.
    """
    return []


@implementer(IVocabularyFactory)
class AllowableContentTypesVocabulary:
    """Vocabulary factory for allowable content types.

    A list of mime-types that can be used as input for textfields.

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

    def __call__(self, context):
        site = getSite()
        items = list(getAllowableContentTypes(site))
        if "text/x-plone-outputfilters-html" in items:
            items.remove("text/x-plone-outputfilters-html")
        items = [SimpleTerm(i, i, i) for i in sorted(items)]
        return SimpleVocabulary(items)


AllowableContentTypesVocabularyFactory = AllowableContentTypesVocabulary()


@implementer(IVocabularyFactory)
class AllowedContentTypesVocabulary:
    """Vocabulary factory for allowed content types.

    A list of mime-types that is allowed to be used as input for textfields.

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
      >>> types = util(context)
      >>> types
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(types.by_token)
      2

      >>> doc = types.by_token['text/plain']
      >>> doc.title, doc.token, doc.value
      ('text/plain', 'text/plain', 'text/plain')
    """

    def __call__(self, context):
        site = getSite()
        items = list(getAllowedContentTypes(site))
        items = [SimpleTerm(i, i, i) for i in sorted(items)]
        return SimpleVocabulary(items)


AllowedContentTypesVocabularyFactory = AllowedContentTypesVocabulary()


@implementer(IVocabularyFactory)
class PortalTypesVocabulary:
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
    (u'Page', 'Document', 'Document')
    """

    def __call__(self, context):
        site = getSite()
        ttool = getToolByName(site, "portal_types", None)
        if ttool is None:
            return SimpleVocabulary([])

        request = aq_get(ttool, "REQUEST", None)
        items = [
            (translate(ttool[t].Title(), context=request), t)
            for t in ttool.listContentTypes()
        ]
        items = [SimpleTerm(i[1], i[1], i[0]) for i in sorted(items)]
        return SimpleVocabulary(items)


PortalTypesVocabularyFactory = PortalTypesVocabulary()


@implementer(IVocabularyFactory)
class UserFriendlyTypesVocabulary:
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
    (u'Page', 'Document', 'Document')
    """

    def __call__(self, context):
        site = getSite()
        ptool = getToolByName(site, "plone_utils", None)
        ttool = getToolByName(site, "portal_types", None)
        if ptool is None or ttool is None:
            return SimpleVocabulary([])

        request = aq_get(ttool, "REQUEST", None)
        items = [
            (translate(ttool[t].Title(), context=request), t)
            for t in ptool.getUserFriendlyTypes()
        ]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


UserFriendlyTypesVocabularyFactory = UserFriendlyTypesVocabulary()


BAD_TYPES = [
    "ATBooleanCriterion",
    "ATCurrentAuthorCriterion",
    "ATDateCriteria",
    "ATDateRangeCriterion",
    "ATListCriterion",
    "ATPathCriterion",
    "ATPortalTypeCriterion",
    "ATReferenceCriterion",
    "ATRelativePathCriterion",
    "ATSelectionCriterion",
    "ATSimpleIntCriterion",
    "ATSimpleStringCriterion",
    "ATSortCriterion",
    "Plone Site",
    "TempFolder",
]


@implementer(IVocabularyFactory)
class ReallyUserFriendlyTypesVocabulary:
    """Vocabulary factory for really user friendly portal types.

    Usage:

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
        <plone.app.vocabularies.PermissiveVocabulary object at ...>

        >>> len(types.by_token)
        2

    Containment is unenforced, to make GenericSetup import validation
    handle validation triggered by Choice.fromUnicode() on insertion:

        >>> non_friendly_type = types.getTermByToken('Plone Site')
        >>> non_friendly_type.title, non_friendly_type.token
        ('Plone Site', 'Plone Site')

        >>> doc = types.by_token['Document']
        >>> doc.title, doc.token, doc.value
        ('Page', 'Document', 'Document')
    """

    def __call__(self, context):
        site = getSite()
        ttool = getToolByName(site, "portal_types", None)
        if ttool is None:
            return SimpleVocabulary([])

        request = aq_get(ttool, "REQUEST", None)
        items = [
            (translate(ttool[t].Title(), context=request), t)
            for t in ttool.listContentTypes()
            if t not in BAD_TYPES
        ]

        # Sort items based on the translated title using unidecode
        items.sort(key=lambda x: unidecode(x[0]).lower())

        terms = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return PermissiveVocabulary(terms)


ReallyUserFriendlyTypesVocabularyFactory = ReallyUserFriendlyTypesVocabulary()
