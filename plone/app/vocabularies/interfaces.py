from zope.interface import Interface, Attribute

class IBrowsableTerm(Interface):
    """ Interface for browsable terms. """

    browse_token = Attribute(
        "token",
        """Token which can be used to get contents of browsable terms in
           queryable sources.

        The value of this attribute must be a non-empty 7-bit string.
        Control characters are not allowed.
        """)

    parent_token = Attribute(
        "token",
        """Token which can be used to get contents of the parent of browsable
           terms in queryable sources.

        The value of this attribute must be a non-empty 7-bit string.
        Control characters are not allowed.
        """)
