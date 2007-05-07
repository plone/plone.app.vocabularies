from zope.interface import implements, alsoProvides
from zope.schema.vocabulary import SimpleTerm
from plone.app.vocabularies.interfaces import IBrowsableTerm
from plone.app.vocabularies.interfaces import ITermWithDescription

class TermWithDescription(SimpleTerm):
    implements(ITermWithDescription)
    
    def __init__(self, value, token, title, description=None):
        super(TermWithDescription, self).__init__(value, token=token, title=title)
        self.description = description

class BrowsableTerm(TermWithDescription):
    def __init__(self, value, token=None, title=None, description=None,
                 browse_token=None, parent_token=None):
        super(BrowsableTerm, self).__init__(value, token=token, 
                                            title=title, description=description)
        self.browse_token = browse_token
        self.parent_token = parent_token
        if browse_token is not None or parent_token is not None:
            alsoProvides(self, IBrowsableTerm)
