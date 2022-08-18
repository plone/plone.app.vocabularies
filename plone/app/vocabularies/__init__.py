from plone.app.vocabularies.interfaces import IPermissiveVocabulary
from plone.app.vocabularies.interfaces import ISlicableVocabulary
from zope.interface import directlyProvides
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import urllib


_token_parse_py3 = getattr(urllib, "parse", None)
_token_parse_py27 = lambda token: urllib.unquote_plus(token).decode("utf8")
parse = _token_parse_py3.unquote if _token_parse_py3 else _token_parse_py27


@implementer(ISlicableVocabulary)
class SlicableVocabulary:
    """
    A tokenized vocabulary in which the results can be sliced.
    This class does not implement a complete vocabulary. Instead you use
    this class as a mixin to your vocabulary class.
    This mixin class expects to be used with something resembling
    a SimpleVocabulary. It accesses internal members like _terms
    """

    def __init__(self, terms=[], *interfaces):
        self._terms = terms
        if interfaces:
            directlyProvides(self, *interfaces)

    def __getitem__(self, start, stop=None):
        if isinstance(start, slice):
            slice_inst = start
            start = slice_inst.start
            stop = slice_inst.stop
        elif not stop:
            return self._terms[start]

        # sliced up
        return self._terms[start:stop]

    def __len__(self):
        return len(self._terms)


@implementer(IPermissiveVocabulary)
class PermissiveVocabulary(SimpleVocabulary):
    """
    Permissive vocabulary for cases of integer-keyed choices or cases
    where vocabulary may mutate later in a transaction to include a
    newly inserted value.
    """

    def __contains__(self, value):
        return True

    def getTermByToken(self, token):
        """
        this works around z3c.form.widget.SequenceWidget.extract()
        pseudo-validation (which is broken for a permissive vocabulary).
        """
        try:
            v = super().getTermByToken(token)
        except LookupError:
            # fallback using dummy term, assumes token==value
            return SimpleTerm(token, title=parse(token))
        return v
