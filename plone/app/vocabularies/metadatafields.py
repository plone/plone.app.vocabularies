from plone.base import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


_FIELD_LABEL = {
    "CreationDate": _("Created on"),
    "Creator": _("Creator"),
    "Description": _("Description"),
    "EffectiveDate": _("Publication date"),
    "end": _("End Date"),
    "exclude_from_nav": _("Excluded from navigation"),
    "ExpirationDate": _("Expiration date"),
    "getObjSize": _("Object Size"),
    "id": _("ID"),
    "is_folderish": _("Folder"),
    "last_comment_date": _("Last comment date"),
    "location": _("Location"),
    "ModificationDate": _("Last modified"),
    "review_state": _("Review state"),
    "start": _("Start Date"),
    "Subject": _("Tags"),
    "Type": _("Type"),
    "total_comments": _("Total comments"),
    "mime_type": _("MIME type"),
}


@implementer(IVocabularyFactory)
class MetaDataFieldsVocabulary:
    """Vocabulary factory for metadata fields

    >>> from zope.component import queryUtility
    >>> from plone.app.vocabularies.tests.base import DummyCatalog
    >>> from plone.app.vocabularies.tests.base import create_context

    >>> context = create_context()

    >>> catalog = DummyCatalog(())
    >>> catalog.schema = lambda: ['ModificationDate', 'review_state', 'SomethingNew']
    >>> context.portal_catalog = catalog

    >>> name = 'plone.app.vocabularies.MetadataFields'
    >>> util = queryUtility(IVocabularyFactory, name)

    >>> fields = util(context)
    >>> fields
    <zope.schema.vocabulary.SimpleVocabulary object at ...>

    >>> len(fields.by_token)
    3

    >>> modification_date = fields.by_token['ModificationDate']
    >>> modification_date.title, modification_date.token, modification_date.value
    (u'Last modified', 'ModificationDate', 'ModificationDate')
    """

    def __call__(self, context):
        cat = getToolByName(context, "portal_catalog")
        items = [
            SimpleTerm(
                column,
                column,
                _FIELD_LABEL[column] if column in _FIELD_LABEL else _(column),
            )
            for column in cat.schema()
        ]
        return SimpleVocabulary(items)


MetaDataFieldsVocabularyFactory = MetaDataFieldsVocabulary()


def get_field_label(field):
    return _FIELD_LABEL.get(field, field)
