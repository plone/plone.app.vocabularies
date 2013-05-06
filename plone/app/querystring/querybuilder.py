import json

from zope.component import getMultiAdapter, getUtility
from zope.i18n import translate

from zope.i18nmessageid import MessageFactory
from zope.publisher.browser import BrowserView


from plone.app.contentlisting.interfaces import IContentListing
from plone.registry.interfaces import IRegistry
from plone.app.querystring import queryparser

from Products.CMFCore.utils import getToolByName
from plone.batching import Batch

from .interfaces import IQuerystringRegistryReader

_ = MessageFactory('plone')


class ContentListingView(BrowserView):
    """BrowserView for displaying query results"""

    def __call__(self, **kw):
        return self.index(**kw)


class QueryBuilder(BrowserView):
    """ This view is used by the javascripts,
        fetching configuration or results"""

    def __init__(self, context, request):
        super(QueryBuilder, self).__init__(context, request)
        self._results = None

    def __call__(self, query, batch=False, b_start=0, b_size=30,
                 sort_on=None, sort_order=None, limit=0, brains=False):
        """If there are results, make the query and return the results"""
        if self._results is None:
            self._results = self._makequery(
                query=query,
                batch=batch,
                b_start=b_start,
                b_size=b_size,
                sort_on=sort_on,
                sort_order=sort_order,
                limit=limit,
                brains=brains)
        return self._results

    def html_results(self, query):
        """html results, used for in the edit screen of a collection,
           used in the live update results"""
        options = dict(original_context=self.context)
        results = self(query, sort_on=self.request.get('sort_on', None),
                       sort_order=self.request.get('sort_order', None),
                       limit=10)

        return getMultiAdapter((results, self.request),
            name='display_query_results')(**options)

    def _makequery(self, query=None, batch=False, b_start=0, b_size=30,
                   sort_on=None, sort_order=None, limit=0, brains=False):
        """Parse the (form)query and return using multi-adapter"""
        parsedquery = queryparser.parseFormquery(
            self.context, query, sort_on, sort_order)
        if not parsedquery:
            if brains:
                return []
            else:
                return IContentListing([])

        catalog = getToolByName(self.context, 'portal_catalog')
        if batch:
            parsedquery['b_start'] = b_start
            parsedquery['b_size'] = b_size
        elif limit:
            parsedquery['sort_limit'] = limit

        if 'path' not in parsedquery:
            parsedquery['path'] = {'query': ''}

        # The Subject field in Plone currently uses a utf-8 encoded string.
        # When a catalog query tries to compare a unicode string from the
        # parsedquery with existing utf-8 encoded string indexes unindexing
        # will fail with a UnicodeDecodeError. To prevent this from happening
        # we always encode the Subject query.
        # XXX: As soon as Plone uses unicode for all indexes, this code can
        # be removed.
        if 'Subject' in parsedquery:
            query = parsedquery['Subject']['query']
            # query can be a unicode string or a list of unicode strings.
            if isinstance(query, unicode):
                parsedquery['Subject']['query'] = query.encode("utf-8")
            elif isinstance(query, list):
                # We do not want to change the collections' own query string,
                # therefore we create a new copy of the list.
                copy_of_query = list(query)
                # Iterate over all query items and encode them if they are
                # unicode strings
                i = 0
                for item in copy_of_query:
                    if isinstance(item, unicode):
                        copy_of_query[i] = item.encode("utf-8")
                    i += 1
                parsedquery['Subject']['query'] = copy_of_query
            else:
                pass

        results = catalog(parsedquery)
        if not brains:
            results = IContentListing(results)
        if batch:
            results = Batch(results, b_size, start=b_start)
        return results

    def number_of_results(self, query):
        """Get the number of results"""
        results = self(query, sort_on=None, sort_order=None, limit=1)
        return translate(_(u"batch_x_items_matching_your_criteria",
                 default=u"${number} items matching your search terms.",
                 mapping={'number': results.actual_result_count}),
                 context=self.request)


class RegistryConfiguration(BrowserView):
    def __call__(self):
        registry = getUtility(IRegistry)
        reader = getMultiAdapter(
            (registry, self.request), IQuerystringRegistryReader)
        data = reader()
        return json.dumps(data)
