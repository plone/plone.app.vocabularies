# -*- coding: utf-8 -*-
from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class SearchIndexesVocabulary(object):
    """Vocabulary factory for search indexes.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context

      >>> name = 'plone.app.vocabularies.SearchIndexes'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> indexes = util(context)
      >>> indexes
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(indexes.by_token)
      3

      >>> term = indexes.by_token['Date']
      >>> term.title, term.token, term.value
      (u'date (newest first)', 'Date', 'Date')
    """

    def __call__(self, context):
        items = []
        items.append((_(u'relevance'), 'relevance'))
        items.append((_(u'date (newest first)'), 'Date'))
        items.append((_(u'alphabetically'), 'sortable_title'))

        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

SearchIndexesVocabularyFactory = SearchIndexesVocabulary()
