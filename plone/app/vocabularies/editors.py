from plone.base.interfaces import IEditingSchema
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


_ = MessageFactory("plone")


@implementer(IVocabularyFactory)
class AvailableEditorsVocabulary:
    def __call__(self, context):
        items = []

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IEditingSchema, prefix="plone", check=False)

        if settings:
            editors = settings.available_editors
            items = [SimpleTerm(e, e, _(e)) for e in editors]
        return SimpleVocabulary(items)


AvailableEditorsVocabularyFactory = AvailableEditorsVocabulary()
