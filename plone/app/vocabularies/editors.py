from Products.CMFPlone.interfaces import IEditingSchema
from plone.registry.interfaces import IRegistry
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility

_ = MessageFactory('plone')


class AvailableEditorsVocabulary(object):
    """Vocabulary factory for available editors in the portal.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import create_context
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.AvailableEditors'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context = create_context()

      >>> tool = DummyTool('portal_properties')
      >>> site_properties = DummyContext()
      >>> available_editors = ['Kupu', 'TinyMCE']
      >>> site_properties.available_editors = available_editors
      >>> tool.site_properties = site_properties
      >>> context.portal_properties = tool

      >>> editors = util(context)
      >>> editors
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(editors.by_token)
      2

      >>> TinyMCE = editors.by_token['TinyMCE']
      >>> TinyMCE.title, TinyMCE.token, TinyMCE.value
      (u'TinyMCE', 'TinyMCE', 'TinyMCE')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IEditingSchema, prefix='plone')
        if settings is not None:
            editors = settings.available_editors
            items = [SimpleTerm(e, e, _(e)) for e in editors]
        return SimpleVocabulary(items)

AvailableEditorsVocabularyFactory = AvailableEditorsVocabulary()
