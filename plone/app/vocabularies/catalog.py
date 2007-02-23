from zope.interface import implements, classProvides
from zope.schema.interfaces import ISource, IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName


class SearchableTextSource(object):
    implements(ISource)
    classProvides(IContextSourceBinder)

    def __init__(self, context):
        self.context = context
        self.catalog = getToolByName(context, "portal_catalog")

    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if self.catalog.getrid(value) is None:
            return False
        return True

    def search(self, query):
        context = self.context
        for char in '?-+*()':
            query = query.replace(char, ' ')
        query = query.split()
        query = " AND ".join(x+"*" for x in query)
        return (x.getPath() for x in self.catalog(SearchableText=query))


class QuerySearchableTextSourceView(object):
    implements(ITerms,
               ISourceQueryView)

    template = ViewPageTemplateFile('searchabletextsource.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getTerm(self, value):
        rid = self.context.catalog.getrid(value)
        brain = self.context.catalog._catalog[rid]
        title = brain.Title
        token = value
        return SimpleTerm(value, token=token, title=title)

    def getValue(self, token):
        if token not in self.context:
            LookupError(token)

        return token

    def render(self, name):
        return self.template(name=name)

    def results(self, name):
        if not name+".search" in self.request.form:
            return None
        query_fieldname = name+".query"
        if query_fieldname in self.request.form:
            query = self.request.form[query_fieldname]
            if query != '':
                return self.context.search(query)
