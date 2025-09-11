from zope.deferredimport import deprecated


deprecated(
    "Import parseQueryString as parseAndModifyFormquery from plone.app.querystring.queryparser instead (will be removed in Plone 7)",
    parseQueryString="plone.app.querystring.queryparser:parseAndModifyFormquery",
)
