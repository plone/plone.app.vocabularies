from plone.app.querystring import queryparser
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from zope.component import getUtilitiesFor


def parseQueryString(context, query):
    parsedquery = queryparser.parseFormquery(context, query)

    index_modifiers = getUtilitiesFor(IParsedQueryIndexModifier)
    for name, modifier in index_modifiers:
        if name in parsedquery:
            new_name, query = modifier(parsedquery[name])
            parsedquery[name] = query
            # if a new index name has been returned, we need to replace
            # the native ones
            if name != new_name:
                del parsedquery[name]
                parsedquery[new_name] = query

    return parsedquery
