# -*- coding: utf-8 -*-
from base64 import urlsafe_b64encode
from plone.app.vocabularies.interfaces import IBrowsableTerm
from plone.app.vocabularies.interfaces import ITermWithDescription
from Products.CMFPlone.utils import safe_unicode
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import six


def safe_encode(value):
    if isinstance(value, six.text_type):
        # no need to use portal encoding for transitional encoding from
        # unicode to ascii. utf-8 should be fine.
        value = value.encode('utf-8')
    return value


def safe_simpleterm_from_value(value):
    """create SimpleTerm from an untrusted value.

    Keyword arguments:
    value -- text or
        value, title tuple

    - token need cleaned up: Vocabulary term tokens *must* be 7 bit values
    - tokens cannot contain newlines
    - anything for display has to be cleaned up, titles *must* be unicode

    >>> st = safe_simpleterm_from_value('Auditorium')
    >>> st.value, st.token, st.title
    ('Auditorium', 'QXVkaXRvcml1bQ==', 'Auditorium')
    """
    untrustedvalue = isinstance(value, tuple) and value or (value, value)
    return SimpleTerm(untrustedvalue[0], urlsafe_b64encode(safe_encode(untrustedvalue[0])), safe_unicode(untrustedvalue[1]))


def safe_simplevocabulary_from_values(values, query=None):
    """Creates (filtered) SimpleVocabulary from iterable of untrusted values.

    Keyword arguments:
    values -- list of values or
        list of value, title tuples or
        dictionary with key: term value, value: term title

    >>> vcb = safe_simplevocabulary_from_values([u'Hörsaal 1', u'Auditorium'])
    >>> horsaal1 = vcb.by_token['SMO2cnNhYWwgMQ==']
    >>> horsaal1.value, horsaal1.token, horsaal1.title
    ('Hörsaal 1', 'SMO2cnNhYWwgMQ==', 'Hörsaal 1')
    >>> vcb = safe_simplevocabulary_from_values(
    ...        {
    ...            u"Hörsaal 1": u"Hörsaal 1",
    ...            u"Auditorium": u"Auditorium",
    ...        }
    ...    )
    >>> horsaal1 = vcb.by_token['SMO2cnNhYWwgMQ==']
    >>> horsaal1.value, horsaal1.token, horsaal1.title
    ('Hörsaal 1', 'SMO2cnNhYWwgMQ==', 'Hörsaal 1')
    """
    untrustedvalues = isinstance(values, dict) and tuple(values.items()) or values
    items = [
        safe_simpleterm_from_value(i)
        for i in untrustedvalues
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
