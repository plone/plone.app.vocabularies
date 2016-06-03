# -*- coding: utf-8 -*-
from binascii import b2a_qp
from plone.app.vocabularies.interfaces import IBrowsableTerm
from plone.app.vocabularies.interfaces import ITermWithDescription
from Products.CMFPlone.utils import safe_unicode
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def safe_encode(value):
    if isinstance(value, unicode):
        # no need to use portal encoding for transitional encoding from
        # unicode to ascii. utf-8 should be fine.
        value = value.encode('utf-8')
    return value


def safe_simpleterm_from_value(value):
    """create SimpleTerm from an untrusted value.

    - token need cleaned up: Vocabulary term tokens *must* be 7 bit values
    - anything for display has to be cleaned up, titles *must* be unicode
    """
    return SimpleTerm(value, b2a_qp(safe_encode(value)), safe_unicode(value))


def safe_simplevocabulary_from_values(values, query=None):
    """Creates (filtered) SimpleVocabulary from iterable of untrusted values.
    """
    items = [
        safe_simpleterm_from_value(i)
        for i in values
        if query is None or safe_encode(query) in safe_encode(i)
    ]
    return SimpleVocabulary(items)


@implementer(ITermWithDescription)
class TermWithDescription(SimpleTerm):
    """
      >>> term = TermWithDescription('value', 'token', 'title')
      >>> term.value, term.token, term.title, term.description
      ('value', 'token', 'title', None)

      >>> term = TermWithDescription('value', 'token', 'title',
      ...                            description='description')
      >>> term.value, term.token, term.title, term.description
      ('value', 'token', 'title', 'description')
    """

    def __init__(self, value, token, title, description=None):
        super(TermWithDescription, self).__init__(
            value,
            token=token,
            title=title
        )
        self.description = description


class BrowsableTerm(TermWithDescription):
    """
      >>> term = BrowsableTerm('value')
      >>> term.value, term.token, term.title, term.description
      ('value', 'value', None, None)
      >>> IBrowsableTerm.providedBy(term)
      False

      >>> term = BrowsableTerm('value', 'token', 'title',
      ...                      description='description',
      ...                      browse_token='browse_token',
      ...                      parent_token='parent_token')
      >>> term.value, term.token, term.title, term.description
      ('value', 'token', 'title', 'description')
      >>> term.browse_token, term.parent_token
      ('browse_token', 'parent_token')
      >>> IBrowsableTerm.providedBy(term)
      True
    """

    def __init__(self, value, token=None, title=None, description=None,
                 browse_token=None, parent_token=None):
        super(BrowsableTerm, self).__init__(
            value,
            token=token,
            title=title,
            description=description
        )
        self.browse_token = browse_token
        self.parent_token = parent_token
        if browse_token is not None or parent_token is not None:
            alsoProvides(self, IBrowsableTerm)
