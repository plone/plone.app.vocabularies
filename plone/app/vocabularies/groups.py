import itertools
from zope.interface import implements, classProvides
from zope.schema.interfaces import ISource, IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

class GroupsSource(object):
    implements(ISource)
    classProvides(IContextSourceBinder)

    def __init__(self, context):
        self.context = context
        self.users = getToolByName(context, "acl_users")

    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if self.get(value) is None:
            return False
        return True

    def search(self, query):
        # XXX: For some reason, this doesn't seem to know how to match on
        # title, only name, and seems to match other random groups if
        # it's unicode
        
        try:
            name = query.encode('ascii')
        except UnicodeEncodeError:
            name = query
        
        return [u['groupid'] for u in self.users.searchGroups(name=name)]
        
    def get(self, value):
        return self.users.getGroupById(value, None)


class GroupsSourceQueryView(object):
    implements(ITerms,
               ISourceQueryView)

    template = ViewPageTemplateFile('searchabletextsource.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getTerm(self, value):
        group = self.context.get(value)
        token = value
        title = value
        if group is not None:
            title = group.getProperty('title', None) or group.getId()
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