from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry

from plone.app.querystring import queryparser
from zope.component import getMultiAdapter, getUtility

from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.app.contentlisting.interfaces import IContentListing
from zope.i18n import translate
import json


class ContentListingView(BrowserView):
    """BrowserView for displaying query results"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, **kw):
        return self.index(**kw)


class QueryBuilder(BrowserView):
    """ This view is used by the javascripts,
        fetching configuration or results"""

    def __init__(self, context, request):
        self._results = None
        self.context = context
        self.request = request

    def __call__(self, query, sort_on=None, sort_order=None):
        """If there are results, make the query and return the results"""
        if self._results is None:
            self._results = self._makequery(query=query,
                                            sort_on=sort_on,
                                            sort_order=sort_order)
        return self._results

    def html_results(self, query):
        """html results, used for in the edit screen of a collection,
           used in the live update results"""
        options = dict(original_context=self.context)
        results = self(query, self.request.get('sort_on', None),
                       self.request.get('sort_order', None))

        return getMultiAdapter((results, self.request),
            name='display_query_results')(
            **options)

    def _makequery(self, query=None, sort_on=None, sort_order=None):
        """Parse the (form)query and return using multi-adapter"""
        parsedquery = queryparser.parseFormquery(self.context,
                                                 query,
                                                 sort_on,
                                                 sort_order)
        if not parsedquery:
            return IContentListing([])

        return getMultiAdapter((self.context, self.request),
            name='searchResults')(query=parsedquery)

    def number_of_results(self, query):
        """Get the number of results"""
        results = self(query, None, None)
        return translate(u"batch_x_items_matching_your_criteria",
                 default=u"${number} items matching your search terms",
                 mapping={'number': len(results)})


class RegistryConfiguration(BrowserView):

    def __init__(self, context, request):
        self._results = None
        self.context = context
        self.request = request

    def __call__(self):
        """Return the registry configuration in JSON format"""
        return json.dumps(IQuerystringRegistryReader(getUtility(IRegistry))())
