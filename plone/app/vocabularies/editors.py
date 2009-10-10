from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName

class AvailableEditorsVocabulary(object):
    """Vocabulary factory for available editors in the portal.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.AvailableEditors'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> tool = DummyTool('portal_properties')
      >>> site_properties = DummyContext()
      >>> available_editors = ['Kupu', 'TinyMCE']
      >>> site_properties.available_editors = available_editors
      >>> tool.site_properties = site_properties
      >>> context2.portal_properties = tool

      >>> editors = util(context1)
      >>> editors
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(editors.by_token)
      2

      >>> TinyMCE = editors.by_token['TinyMCE']
      >>> TinyMCE.title, TinyMCE.token, TinyMCE.value
      ('TinyMCE', 'TinyMCE', 'TinyMCE')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        pprop = getToolByName(context, 'portal_properties', None)

        if pprop is None:
            return None

        editors = pprop.site_properties.available_editors
        items = [SimpleTerm(e, e, e) for e in editors]
        return SimpleVocabulary(items)

AvailableEditorsVocabularyFactory = AvailableEditorsVocabulary()
