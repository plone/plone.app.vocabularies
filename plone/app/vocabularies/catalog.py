from BTrees.IIBTree import intersection
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.vocabularies import SlicableVocabulary
from plone.app.vocabularies.terms import BrowsableTerm
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from plone.app.vocabularies.utils import parseQueryString
from plone.base.utils import safe_text
from plone.memoize import request
from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ZCTextIndex.ParseTree import ParseError
from z3c.formwidget.query.interfaces import IQuerySource
from zope.browser.interfaces import ITerms
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import itertools
import json
import os
import warnings


try:
    from zope.formlib.interfaces import ISourceQueryView
except ImportError:
    from zope.interface import Interface

    class ISourceQueryView(Interface):
        pass


def parse_query(query, path_prefix=""):
    """Parse the query string and turn it into a dictionary for querying the
    catalog.

    We want to find anything which starts with the given string, so we add
    a * at the end of words.

    >>> parse_query('foo')
    {'SearchableText': 'foo*'}

    If we have more than one word, each of them should have the * and
    they should be combined with the AND operator.

    >>> parse_query('foo bar')
    {'SearchableText': 'foo* AND bar*'}

    We also filter out some special characters. They are handled like
    spaces and seperate words from each other.

    >>> parse_query('foo +bar some-thing')
    {'SearchableText': 'foo* AND bar* AND some* AND thing*'}

    >>> parse_query('what? (spam) *ham')
    {'SearchableText': 'what* AND spam* AND ham*'}

    You can also limit searches to paths, if you only supply the path,
    then all contents of that folder will be searched. If you supply
    additional search words, then all subfolders are searched as well.

    >>> expected = {'path': {'query': '/dummy', 'depth': 1}}
    >>> parse_query('path:/dummy') == expected
    True

    >>> expected = {'path': {'query': '/dummy'}, 'SearchableText': 'bar*'}
    >>> parse_query('bar path:/dummy') == expected
    True

    >>> expected = {'path': {'query': '/dummy'}, 'SearchableText': 'foo*'}
    >>> parse_query('path:/dummy foo') == expected
    True

    If you supply more then one path, then only the last one is used.

    >>> expected = {'path': {'query': '/spam', 'depth': 1}}
    >>> parse_query('path:/dummy path:/spam') == expected
    True

    You can also provide a prefix for the path. This is useful for virtual
    hosting.

    >>> expected = {'path': {'query': '/portal/dummy', 'depth': 1}}
    >>> parse_query('path:/dummy', path_prefix='/portal') == expected
    True

    """
    query_parts = query.split()
    query = {"SearchableText": []}
    for part in query_parts:
        if part.startswith("path:"):
            path = part[5:]
            query["path"] = {"query": path}
        else:
            query["SearchableText"].append(part)
    text = " ".join(query["SearchableText"])
    for char in "?-+*()":
        text = text.replace(char, " ")
    query["SearchableText"] = " AND ".join(x + "*" for x in text.split())
    if "path" in query:
        if query["SearchableText"] == "":
            del query["SearchableText"]
            query["path"]["depth"] = 1
        query["path"]["query"] = path_prefix + query["path"]["query"]
    return query


@implementer(ISource)
@provider(IContextSourceBinder)
class SearchableTextSource:
    """
    >>> from plone.app.vocabularies.tests.base import Brain
    >>> from plone.app.vocabularies.tests.base import DummyCatalog
    >>> from plone.app.vocabularies.tests.base import create_context
    >>> from plone.app.vocabularies.tests.base import DummyTool

    >>> context = create_context()

    >>> catalog = DummyCatalog(('/1234', '/2345'))
    >>> context.portal_catalog = catalog

    >>> tool = DummyTool('portal_url')
    >>> def getPortalPath():
    ...     return '/'
    >>> tool.getPortalPath = getPortalPath
    >>> context.portal_url = tool

    >>> source = SearchableTextSource(context)
    >>> source
    <plone.app.vocabularies.catalog.SearchableTextSource object at ...>

    >>> '1234' in source, '1' in source
    (True, False)

    >>> source.search('')
    []

    >>> source.search('error')
    []

    >>> source.search('foo')
    <generator object ...>

    >>> list(source.search('foo'))
    ['1234', '2345']

    >>> list(source.search('bar path:/dummy'))
    ['/dummy', '1234', '2345']

    >>> u'' in source
    True

    >>> source = SearchableTextSource(context, default_query='default')
    >>> list(source.search(''))
    ['1234', '2345']
    """

    def __init__(self, context, base_query={}, default_query=None):
        self.context = context
        self.base_query = base_query
        self.default_query = default_query
        self.catalog = getToolByName(context, "portal_catalog")
        self.portal_tool = getToolByName(context, "portal_url")
        self.portal_path = self.portal_tool.getPortalPath()
        self.encoding = "utf-8"

    def __contains__(self, value):
        """Return whether the value is available in this source"""
        if not value:
            return True
        elif self.catalog.getrid(self.portal_path + value) is None:
            return False
        return True

    def search(self, query_string):
        query = self.base_query.copy()
        if query_string == "":
            if self.default_query is not None:
                query.update(parse_query(self.default_query, self.portal_path))
            else:
                return []
        else:
            query.update(parse_query(query_string, self.portal_path))

        try:
            results = (
                x.getPath()[len(self.portal_path) :] for x in self.catalog(**query)
            )
        except ParseError:
            return []

        if "path" in query:
            path = query["path"]["query"][len(self.portal_path) :]
            if path != "":
                return itertools.chain((path,), results)
        return results


@implementer(IContextSourceBinder)
class SearchableTextSourceBinder:
    """Use this to instantiate a new SearchableTextSource with custom
    parameters. For example:

    target_folder = schema.Choice(
        title=_(u'Target folder'),
        description=_(u'As a path relative to the portal root'),
        required=True,
        source=SearchableTextSourceBinder({'is_folderish' : True}),
        )

    This ensures that the is_folderish=True is always in the query used.

      >>> query = {'query': 'query'}

      >>> binder = SearchableTextSourceBinder(query)
      >>> binder
      <plone.app.vocabularies.catalog.SearchableTextSourceBinder object at ...>

      >>> binder.query == query
      True

      >>> from plone.app.vocabularies.tests.base import Brain
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> context = create_context()

      >>> tool = DummyTool('portal_catalog')
      >>> context.portal_catalog = tool

      >>> tool = DummyTool('portal_url')
      >>> def getPortalPath():
      ...     return '/'
      >>> tool.getPortalPath = getPortalPath
      >>> context.portal_url = tool

      >>> source = binder(context)
      >>> source
      <plone.app.vocabularies.catalog.SearchableTextSource object at ...>

      >>> source.base_query == query
      True
    """

    def __init__(self, query, default_query=None):
        self.query = query
        self.default_query = default_query

    def __call__(self, context):
        return SearchableTextSource(
            context, base_query=self.query.copy(), default_query=self.default_query
        )


@implementer(ITerms, ISourceQueryView)
class QuerySearchableTextSourceView:
    """
    >>> from plone.app.vocabularies.tests.base import DummyCatalog
    >>> from plone.app.vocabularies.tests.base import create_context
    >>> from plone.app.vocabularies.tests.base import DummyTool
    >>> from plone.app.vocabularies.tests.base import Request

    >>> context = create_context()

    >>> rids = ('/1234', '/2345', '/dummy/1234')
    >>> tool = DummyCatalog(rids)
    >>> context.portal_catalog = tool

    >>> tool = DummyTool('portal_url')
    >>> def getPortalPath():
    ...     return '/dummy'
    >>> tool.getPortalPath = getPortalPath
    >>> context.portal_url = tool

    >>> source = SearchableTextSource(context)
    >>> source
    <plone.app.vocabularies.catalog.SearchableTextSource object at ...>

    >>> view = QuerySearchableTextSourceView(source, Request())
    >>> view
    <plone.app.vocabularies.catalog.QuerySearchableTextSourceView object ...>

    >>> view.getValue('a')
    Traceback (most recent call last):
    ...
    LookupError: a

    >>> view.getValue('/1234')
    '/1234'

    >>> view.getTerm(None) is None
    True

    >>> view.getTerm('1234')
    <plone.app.vocabularies.terms.BrowsableTerm object at ...>

    >>> view.getTerm('/1234')
    <plone.app.vocabularies.terms.BrowsableTerm object at ...>

    >>> template = view.render(name='t')
    >>> u'<input type="text" name="t.query" value="" />' in template
    True

    >>> u'<input type="submit" name="t.search" value="Search" />' in template
    True

    >>> request = Request(form={'t.search' : True, 't.query' : 'value'})
    >>> view = QuerySearchableTextSourceView(source, request)
    >>> sorted(view.results('t'))
    ['', '', '/1234']

    >>> request = Request(form={'t.search' : True, 't.query' : 'value',
    ...                         't.browse.foo' : '/foo'})
    >>> view = QuerySearchableTextSourceView(source, request)
    >>> sorted(view.results('t'))
    ['', '', '/1234', 'foo']

    Titles need to be unicode:
    >>> view.getTerm(list(view.results('t'))[0]).title
    u'/foo'
    """

    template = ViewPageTemplateFile("searchabletextsource.pt")

    def __init__(self, context, request):
        msg = (
            "QuerySearchableTextSourceView is deprecated and will be "
            "removed on Plone 6"
        )
        warnings.warn(msg, DeprecationWarning)
        self.context = context
        self.request = request

    def getTerm(self, value):
        if not value:
            return None
        if (not self.context.portal_path.endswith("/")) and (not value.startswith("/")):
            value = "/" + value
        # get rid for path
        rid = self.context.catalog.getrid(self.context.portal_path + value)
        # first some defaults
        token = value
        title = value
        browse_token = None
        parent_token = None
        if rid is not None:
            # fetch the brain from the catalog
            brain = self.context.catalog._catalog[rid]
            title = brain.Title
            # title = brain.Title
            if brain.is_folderish:
                browse_token = value
            parent_token = "/".join(value.split("/")[:-1])
        return BrowsableTerm(
            value,
            token=token,
            title=title,
            description=value,
            browse_token=browse_token,
            parent_token=parent_token,
        )

    def getValue(self, token):
        if token not in self.context:
            raise LookupError(token)
        return token

    def render(self, name):
        return self.template(name=name)

    def results(self, name):
        query = ""

        # check whether the normal search button was pressed
        if name + ".search" in self.request.form:
            query_fieldname = name + ".query"
            if query_fieldname in self.request.form:
                query = self.request.form[query_fieldname]

        # check whether a browse button was pressed
        browse_prefix = name + ".browse."
        browse = tuple(x for x in self.request.form if x.startswith(browse_prefix))
        if len(browse) == 1:
            path = browse[0][len(browse_prefix) :]
            query = "path:" + path
            results = self.context.search(query)
            if name + ".omitbrowsedfolder" in self.request.form:
                results = filter(lambda x: x != path, results)
        else:
            results = self.context.search(query)

        return results


@implementer(IVocabularyFactory)
class KeywordsVocabulary:
    """Vocabulary factory listing all catalog keywords from the 'Subject' index

    >>> from plone.app.vocabularies.tests.base import DummyCatalog
    >>> from plone.app.vocabularies.tests.base import create_context
    >>> from plone.app.vocabularies.tests.base import DummyContent
    >>> from plone.app.vocabularies.tests.base import Request
    >>> from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex  # noqa

    >>> context = create_context()

    First test bytes vocabularies
    >>> rids = ('/1234', '/2345', '/dummy/1234')
    >>> tool = DummyCatalog(rids)
    >>> context.portal_catalog = tool
    >>> index = KeywordIndex('Subject')
    >>> done = index._index_object(
    ...     1,
    ...     DummyContent('ob1', [b'foo', b'bar', b'baz']), attr='Subject'
    ... )
    >>> done = index._index_object(
    ...     2,
    ...     DummyContent(
    ...         'ob2',
    ...         [b'blee', b'bar', u'non-åscii'.encode('utf8')]),
    ...         attr='Subject',
    ... )
    >>> tool.indexes['Subject'] = index
    >>> vocab = KeywordsVocabulary()
    >>> result = vocab(context)

    Value type is kept ...
    >>> expected = [b'bar', b'baz', b'blee', b'foo', u'non-åscii'.encode('utf8')]
    >>> sorted(result.by_value) == expected
    True

    but tokens are base64 encoded text
    >>> expected = ['YmF6', 'YmFy', 'YmxlZQ==', 'Zm9v', 'bm9uLcOlc2NpaQ==']
    >>> sorted(result.by_token) == expected
    True

    >>> result.getTermByToken(expected[-1]).title == u'non-åscii'
    True

    Testing unicode vocabularies
    First clear the index. Comparing bytes to str objects fails.
    >>> index.clear()
    >>> done = index._index_object(
    ...     1,
    ...     DummyContent('obj1', [u'äüö', u'nix']), attr='Subject'
    ... )
    >>> tool.indexes['Subject'] = index
    >>> vocab = KeywordsVocabulary()
    >>> result = vocab(context)
    >>> expected = ['bml4', 'w6TDvMO2']
    >>> sorted(result.by_token) == expected
    True
    >>> set(result.by_value) == {u'nix', u'äüö'}
    True
    >>> result.getTermByToken(expected[0]).title == u'nix'
    True

    """

    # Allow users to customize the index to easily create
    # KeywordVocabularies for other keyword indexes
    keyword_index = "Subject"
    path_index = "path"

    def section(self, context):
        """gets section from which subjects are used."""
        registry = queryUtility(IRegistry)
        if registry is None:
            return None
        if registry.get("plone.subjects_of_navigation_root", False):
            portal = getToolByName(context, "portal_url").getPortalObject()
            return getNavigationRootObject(context, portal)
        return None

    def all_keywords(self, kwfilter):
        site = getSite()
        self.catalog = getToolByName(site, "portal_catalog", None)
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex(self.keyword_index)
        return safe_simplevocabulary_from_values(index._index, query=kwfilter)

    def keywords_of_section(self, section, kwfilter):
        """Valid keywords under the given section."""
        pcat = getToolByName(section, "portal_catalog")
        cat = pcat._catalog
        path_idx = cat.indexes[self.path_index]
        tags_idx = cat.indexes[self.keyword_index]
        result = []
        # query all oids of path - low level
        pquery = {
            self.path_index: {
                "query": "/".join(section.getPhysicalPath()),
                "depth": -1,
            }
        }
        kwfilter = safe_text(kwfilter)
        # uses internal zcatalog specific details to quickly get the values.
        path_result, info = path_idx._apply_index(pquery)
        for tag in tags_idx.uniqueValues():
            if kwfilter and kwfilter not in safe_text(tag):
                continue
            tquery = {self.keyword_index: tag}
            tags_result, info = tags_idx._apply_index(tquery)
            if intersection(path_result, tags_result):
                result.append(tag)
        # result should be sorted, because uniqueValues are.
        return safe_simplevocabulary_from_values(result)

    def __call__(self, context, query=None):
        section = self.section(context)
        if section is None:
            return self.all_keywords(query)
        return self.keywords_of_section(section, query)


KeywordsVocabularyFactory = KeywordsVocabulary()


class CatalogVocabulary(SlicableVocabulary):
    # We want to get rid of this and use CatalogSource instead,
    # but we can't in Plone versions that support
    # plone.app.widgets < 1.6.0

    @classmethod
    def fromItems(cls, query, context, *interfaces):
        return cls(query)

    fromValues = fromItems

    @classmethod
    def createTerm(cls, brain, context):
        return SimpleTerm(brain, brain.UID, brain.UID)

    def __init__(self, query, *interfaces):
        self.query = query

    @property
    @memoize
    def catalog(self):
        return getToolByName(getSite(), "portal_catalog")

    @property
    @memoize
    def brains(self):
        try:
            return self.catalog(**self.query)
        except ParseError:
            # a parseError: Query contains only common words may happen,
            # semantically this means we want all result w/o SearchableText
            if "SearchableText" in self.query:
                del self.query["SearchableText"]
                return self.catalog(**self.query)
            raise

    def __iter__(self):
        for brain in self.brains:
            yield self.createTerm(brain, None)

    def __contains__(self, value):
        if isinstance(value, str):
            # perhaps it's already a uid
            uid = value
        else:
            uid = IUUID(value)
        query = self.query.copy()
        query["UID"] = uid
        return len(self.catalog(**query)) > 0

    def __len__(self):
        return len(self.brains)

    def __getitem__(self, index):
        if isinstance(index, slice):
            slice_inst = index
            start = slice_inst.start
            stop = slice_inst.stop
            return [self.createTerm(brain, None) for brain in self.brains[start:stop]]
        else:
            return self.createTerm(self.brains[index], None)

    def getTerm(self, value):
        if not isinstance(value, str):
            # here we have a content and fetch the uuid as hex value
            value = IUUID(value)
        query = {"UID": value}
        brains = self.catalog(**query)
        for b in brains:
            return self.createTerm(b, None)

    getTermByToken = getTerm


@implementer(IVocabularyFactory)
class CatalogVocabularyFactory:
    """
    Test application of Navigation Root:

      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyUrlTool
      >>> from plone.app.vocabularies.tests.base import DummyCatalog
      >>> class DummyPathCatalog(DummyCatalog):
      ...     def __call__(self, **query):
      ...         if 'path' in query and 'query' in query['path']:
      ...             return [v for v in self.values() if
      ...                     v.getPath().startswith(query['path']['query'])]
      ...         return self.values()
      >>> catalog = DummyPathCatalog(['/abcd', '/defg', '/dummy/sub-site',
      ...                             '/dummy/sub-site/ghij'])
      >>> context = create_context()
      >>> context.portal_catalog = catalog
      >>> context.portal_url = DummyUrlTool(context)
      >>> factory = CatalogVocabularyFactory()

      >>> sorted(t.token for t in factory(context))
      ['/abcd', '/defg', '/dummy/sub-site', '/dummy/sub-site/ghij']

      >>> from plone.app.vocabularies.tests.base import DummyNavRoot
      >>> nav_root = DummyNavRoot('sub-site', parent=context)
      >>> [t.token for t in factory(nav_root)]
      ['/dummy/sub-site', '/dummy/sub-site/ghij']

    """

    # We want to get rid of this and use CatalogSource instead,
    # but we can't in Plone versions that support
    # plone.app.widgets < 1.6.0

    def __call__(self, context, query=None):
        parsed = {}
        if query:
            parsed = parseQueryString(context, query["criteria"])
            if "sort_on" in query:
                parsed["sort_on"] = query["sort_on"]
            if "sort_order" in query:
                parsed["sort_order"] = str(query["sort_order"])

        # If no path is specified check if we are in a sub-site and use that
        # as the path root for catalog searches
        if "path" not in parsed:
            site = getSite()
            nav_root = getNavigationRootObject(context, site)
            site_path = site.getPhysicalPath()
            if nav_root and nav_root.getPhysicalPath() != site_path:
                parsed["path"] = {
                    "query": "/".join(nav_root.getPhysicalPath()),
                    "depth": -1,
                }
        return CatalogVocabulary.fromItems(parsed, context)


def request_query_cache_key(func, vocab):
    return json.dumps([vocab.query, vocab.text_search_index, vocab.title_template])


@implementer(IQuerySource, IVocabularyFactory)
class StaticCatalogVocabulary(CatalogVocabulary):
    """Catalog Vocabulary for static queries of content based on a fixed query.
    Intended for use in a zope.schema, e.g.:

        my_relation = RelationChoice(
            title="Custom Relation",
            vocabulary=StaticCatalogVocabulary({
                "portal_type": "Document",
                "review_state": "published",
            })
        )

    Can be used with TextLine values (to store a UUID) or
    Relation/RelationChoice values (to create a z3c.relationfield style
    relation). This vocabulary will work with a variety of selection widgets,
    and provides a text search method to work with the
    plone.app.z3cform.widget.AjaxSelectWidget.

    This vocabulary can be used to make a named vocabulary with a factory
    function:

        from zope.interface import provider
        from zope.schema.interfaces import IVocabularyFactory


        @provider(IVocabularyFactory)
        def my_vocab_factory(context):
            return StaticCatalogVocabulary({
                'portal_type': 'Event',
                'path': '/'.join(context.getPhysicalPath())
            })

    The default item title looks like "Object Title (/path/to/object)", but this
    can be customized by passing a format string as the "title_template"
    parameter. The format string has "brain" and "path" arguments available:

        MY_VOCABULARY = StaticCatalogVocabulary(
            {'portal_type': 'Event'},
            title_template="{brain.Type}: {brain.Title} at {path}"
        )

    When using this vocabulary for dynamic queries, e.g. with the
    AjaxSelectWidget, you can customize the index searched using the
    "text_search_index" parameter. By default it uses the "SearchableText"
    index, but you could have your vocabulary search on "Title" instead:

        from plone.autoform import directives
        from plone.app.z3cform.widget import AjaxSelectFieldWidget


        directives.widget(
            'my_relation',
            AjaxSelectFieldWidget,
            vocabulary=StaticCatalogVocabulary(
                {'portal_type': 'Event'},
                text_search_index="Title",
                title_template="{brain.Type}: {brain.Title} at {path}"
            )
        )

    This vocabulary lazily caches the result set for the base query on the
    request to optimize performance.

    Here are some doctests::

      >>> from plone.app.vocabularies.tests.base import Brain
      >>> from plone.app.vocabularies.tests.base import DummyCatalog
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> context = create_context()

      >>> catalog = DummyCatalog(('/1234', '/2345'))
      >>> context.portal_catalog = catalog

      >>> tool = DummyTool('portal_url')
      >>> def getPortalPath():
      ...     return '/'
      >>> tool.getPortalPath = getPortalPath
      >>> context.portal_url = tool

      >>> vocab = StaticCatalogVocabulary({'portal_type': ['Document']})
      >>> vocab
      <plone.app.vocabularies.catalog.StaticCatalogVocabulary object at ...>

      >>> vocab.search('')
      <zope.schema.vocabulary.SimpleVocabulary object at ...>
      >>> list(vocab.search(''))
      []

      >>> vocab.search('foo')
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> [(t.title, t.value) for t in vocab.search('foo')]
      [(u'BrainTitle (/1234)', '/1234'), (u'BrainTitle (/2345)', '/2345')]

    We strip out the site path from the rendered path in the title template:

      >>> catalog = DummyCatalog(('/site/1234', '/site/2345'))
      >>> context.portal_catalog = catalog
      >>> vocab = StaticCatalogVocabulary({'portal_type': ['Document']})
      >>> [(t.title, t.value) for t in vocab.search('bar')]
      [(u'BrainTitle (/site/1234)', '/site/1234'),
       (u'BrainTitle (/site/2345)', '/site/2345')]

      >>> context.__name__ = 'site'
      >>> vocab = StaticCatalogVocabulary({'portal_type': ['Document']})
      >>> [(t.title, t.value) for t in vocab.search('bar')]
      [(u'BrainTitle (/1234)', '/site/1234'),
       (u'BrainTitle (/2345)', '/site/2345')]

    The title template can be customized:

      >>> vocab.title_template = "{url} {brain.UID} - {brain.Title} {path}"
      >>> [(t.title, t.value) for t in vocab.search('bar')]
      [(u'proto:/site/1234 /site/1234 - BrainTitle /1234', '/site/1234'),
       (u'proto:/site/2345 /site/2345 - BrainTitle /2345', '/site/2345')]

    """

    title_template = "{brain.Title} ({path})"
    text_search_index = "SearchableText"

    def __init__(self, query, text_search_index=None, title_template=None):
        self.query = query
        if text_search_index:
            self.text_search_index = text_search_index
        if title_template:
            self.title_template = title_template

    @property
    @memoize
    def nav_root_path(self):
        site = getSite()
        nav_root = getNavigationRootObject(site, site)
        return "/".join(nav_root.getPhysicalPath())

    def get_brain_path(self, brain):
        nav_root_path = self.nav_root_path
        path = brain.getPath()
        if path.startswith(nav_root_path):
            path = path[len(nav_root_path) :]
        return path

    @staticmethod
    def get_request():
        return getRequest()

    @property
    @request.cache(get_key=request_query_cache_key, get_request="self.get_request()")
    def brains(self):
        return self.catalog(**self.query)

    def createTerm(self, brain, context=None):
        return SimpleTerm(
            value=brain.UID,
            token=brain.UID,
            title=safe_text(
                self.title_template.format(
                    brain=brain,
                    path=self.get_brain_path(brain),
                    url=brain.getURL(),
                )
            ),
        )

    def search(self, query):
        """Required by plone.app.content.browser.vocabulary for simple queryable
        vocabs, e.g. for AJAXSelectWidget."""
        if not query:
            return SimpleVocabulary([])

        if not query.endswith(" "):
            query += "*"
        query = {self.text_search_index: query}
        query.update(self.query)
        brains = self.catalog(**query)
        return SimpleVocabulary([self.createTerm(b) for b in brains])


@implementer(ISource)
class CatalogSource:
    """Catalog source for use with Choice fields.

    When instantiating the source, you can pass keyword arguments
    which will become the catalog query used to find terms.

    e.g.:

      image = Choice(
          title=u'Image',
          source=CatalogSource(portal_type='Image'),
          )

    The `__contains__` method is used during validation to
    make sure the selected item is found with the specified query.

    The `search_catalog` method is used by plone.app.widgets
    to retrieve catalog brains for this source's query augmented by
    input from the user interacting with the widget.

    Tests:

      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from OFS.SimpleItem import SimpleItem
      >>> class DummyCatalog(SimpleItem):
      ...     def __init__(self, values):
      ...         self.values = values
      ...     def __call__(self, query):
      ...         if 'foo' in query and query['foo'] == 'bar':
      ...             return self.values
      >>> context = create_context()
      >>> context.portal_catalog = DummyCatalog(['asdf'])
      >>> source = CatalogSource(foo='bar')

      >>> 'asdf' in source
      True

      >>> source.search_catalog({'foo': 'baz'})
      ['asdf']

    """

    def __init__(self, context=None, **query):
        self.query = query

    def __contains__(self, value):
        """used during validation to make sure the selected item is found with
        the specified query.

        value can be either a string (hex value of uuid or path) or a plone
        content object.
        """
        if not isinstance(value, str):
            # here we have a content and fetch the uuid as hex value
            value = IUUID(value)
        # else we have uuid hex value or path

        if value.startswith("/"):
            # it is a path query
            site = getSite()
            site_path = "/".join(site.getPhysicalPath())
            path = os.path.join(site_path, value.lstrip("/"))
            query = {"path": {"query": path, "depth": 0}}
        else:
            # its a uuid
            query = {"UID": value}
        return bool(self.search_catalog(query))

    def search_catalog(self, user_query):
        query = user_query.copy()
        query.update(self.query)
        catalog = getToolByName(getSite(), "portal_catalog")
        return catalog(query)
