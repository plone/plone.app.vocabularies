from zope.interface import implements, classProvides
from zope.schema.interfaces import ISource, IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName


def parse_query(query, portal_path=""):
    """ Parse the query string and turn it into a dictionary for querying the
        catalog.

        >>> parse_query('foo')
        {'SearchableText': 'foo*'}
    """
    query_parts = query.split()
    query = {'SearchableText': []}
    for part in query_parts:
        if part.startswith('path:'):
            path = part[5:]
            query['path'] = {'query': path}
        else:
            query['SearchableText'].append(part)
    text = " ".join(query['SearchableText'])
    for char in '?-+*()':
        text = text.replace(char, ' ')
    query['SearchableText'] = " AND ".join(x+"*" for x in text.split())
    if query.has_key('path'):
        if not len(query['SearchableText']):
            query["path"]["depth"] = 1
        query["path"]["query"] = portal_path + query["path"]["query"]
    return query

class SearchableTextSource(object):
    implements(ISource)
    classProvides(IContextSourceBinder)

    def __init__(self, context):
        self.context = context
        self.catalog = getToolByName(context, "portal_catalog")
        self.portal_tool = getToolByName(context, "portal_url")
        self.portal_path = self.portal_tool.getPortalPath()

    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if self.catalog.getrid(self.portal_path + value) is None:
            return False
        return True

    def search(self, query):
        query = parse_query(query, self.portal_path)
        return (x.getPath()[len(self.portal_path):] for x in self.catalog(**query))


class QuerySearchableTextSourceView(object):
    implements(ITerms,
               ISourceQueryView)

    template = ViewPageTemplateFile('searchabletextsource.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getTerm(self, value):
        rid = self.context.catalog.getrid(self.context.portal_path + value)
        if rid is not None:
            brain = self.context.catalog._catalog[rid]
            title = brain.Title
        else:
            title = value
        token = value
        return SimpleTerm(value, token=token, title=title)

    def getValue(self, token):
        if token not in self.context:
            LookupError(token)

        return token

    def render(self, name):
        return self.template(name=name)

    def results(self, name):
        # check whether the normal search button was pressed
        if name+".search" in self.request.form:
            query_fieldname = name+".query"
            if query_fieldname in self.request.form:
                query = self.request.form[query_fieldname]
                if query != '':
                    return self.context.search(query)

        # check whether a browse button was pressed
        browse_prefix = name+".browse."
        browse = tuple(x for x in self.request.form
                       if x.startswith(browse_prefix))
        if len(browse) == 1:
            path = browse[0][len(browse_prefix):]
            return self.context.search("path:"+path)
