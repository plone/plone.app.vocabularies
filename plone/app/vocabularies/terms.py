from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleTerm
from plone.app.vocabularies.interfaces import IBrowsableTerm


class BrowsableTerm(SimpleTerm):
    def __init__(self, value, token=None, title=None,
                 browse_token=None, parent_token=None):
        super(BrowsableTerm, self).__init__(value, token=token, title=title)
        self.browse_token = browse_token
        self.parent_token = parent_token
        if browse_token is not None or parent_token is not None:
            alsoProvides(self, IBrowsableTerm)
