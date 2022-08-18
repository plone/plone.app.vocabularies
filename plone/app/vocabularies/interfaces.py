from zope.interface import Attribute
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyTokenized


class ITermWithDescription(Interface):
    """A term which carries an additional description"""

    description = Attribute(
        "description",
        """Description of the term, which will be displayed to distinguish
           between terms with similar labels.
        """,
    )


class IBrowsableTerm(Interface):
    """A term which may be browsed. This interface is only applied to
    terms which are actually browsable (e.g. those representing folders).
    """

    browse_token = Attribute(
        "browse_token",
        """Token which can be used to get contents of browsable terms in
           queryable sources.

        The value of this attribute must be a non-empty 7-bit string.
        Control characters are not allowed.
        """,
    )

    parent_token = Attribute(
        "parent_token",
        """Token which can be used to get contents of the parent of browsable
           terms in queryable sources.

        The value of this attribute must be a non-empty 7-bit string.
        Control characters are not allowed.
        """,
    )


class ISlicableVocabulary(IVocabularyTokenized):
    def __getitem__(start, stop):
        """return a slice of the results"""


class IPermissiveVocabulary(IVocabularyTokenized):
    """Vocabulary with permissive validation of containment"""

    def __contains__(self, value):
        """
        Always returns true, for any value; useful for cases where
        validation of containment creates practical problems (e.g.
        vocabulary about to be mutated with insertion of a value not
        yet within).
        """
