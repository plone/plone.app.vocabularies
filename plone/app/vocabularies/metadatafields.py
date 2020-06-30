# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


_FIELD_LABEL = {
    'CreationDate': _('Created on'),
    'Creator': _('Creator'),
    'Description': _('Description'),
    'EffectiveDate': _('Publication date'),
    'end': _('End Date'),
    'exclude_from_nav': _('Excluded from navigation'),
    'ExpirationDate': _('Expiration date'),
    'getObjSize': _('Object Size'),
    'id': _('ID'),
    'is_folderish': _('Folder'),
    'last_comment_date': _('Last comment date'),
    'location': _('Location'),
    'ModificationDate': _('Last modified'),
    'review_state': _('Review state'),
    'start': _('Start Date'),
    'Subject': _('Tags'),
    'Type': _('Type'),
    'total_comments': _('Total comments'),
    'mime_type': _('MIME type'),
}


@implementer(IVocabularyFactory)
class MetaDataFieldsVocabulary(object):

    def __call__(self, context):
        cat = getToolByName(context, 'portal_catalog')
        items = [
            SimpleTerm(column, column, _FIELD_LABEL[column] if column in _FIELD_LABEL else _(column))
            for column in cat.schema()
        ]
        return SimpleVocabulary(items)


MetaDataFieldsVocabularyFactory = MetaDataFieldsVocabulary()


def get_field_label(field):
    return _FIELD_LABEL.get(field, field)
