from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry

from plone.app.querystring import queryparser
from zope.component import getMultiAdapter, getUtility
from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.app.contentlisting.interfaces import IContentListing
from zope.i18n import translate
import json


class ContentListingView(BrowserView):

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

    def __call__(self, query):
        if self._results is None:
            self._results = self._makequery(query=query)
        return self._results

    def html_results(self, query):
        options = dict(original_context=self.context)
        return getMultiAdapter((self(query), self.request),
            name='display_query_results')(
            **options)

    def _makequery(self, query=None):
        parsedquery = queryparser.parseFormquery(self.context, query)
        if not parsedquery:
            return IContentListing([])
        return getMultiAdapter((self.context, self.request),
            name='searchResults')(query=parsedquery)

    def number_of_results(self, query):
        return translate(u"batch_x_items_matching_your_criteria",
                 default=u"${number} items matching your search terms",
                 mapping={'number': len(self(query))})


class RegistryConfiguration(BrowserView):

    def __init__(self, context, request):
        self._results = None
        self.context = context
        self.request = request

    def __call__(self):
        return json.dumps(IQuerystringRegistryReader(getUtility(IRegistry))())
