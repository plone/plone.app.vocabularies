from plone.app.vocabularies.registry import IVocabularyRegistry
from zope.component import getUtility
from zope.configuration import fields as configuration_fields
from zope.interface import Interface
from zope.schema import TextLine


class IVocabularyDirective(Interface):
    """Directive which registers a new vocabulary."""

    name = TextLine(
        title=u'Name',
        description=u'Convenience lookup name for this vocabulary',
        required=True,
    )

    factory = configuration_fields.GlobalObject(
        title=u'The factory for this vocabulary',
        required=True,
    )

    permission = TextLine(
        title=u'Permission',
        description=u'Optional protection of vocabulary',
        required=False,
    )


def VocabularyDirective(_context, name, factory, permission=None):

    # debug
    print(
        "\n*** VocabularyDirective. name, factory, permission: ",
        name, factory, permission
    )

    vocabularyRegistry = getUtility(IVocabularyRegistry)

    if permission:
        vocabularyRegistry.registerVocabulary(
            name=name,
            factory=factory,
            permission="Modify portal content"
        )
    else:
        vocabularyRegistry.registerVocabulary(
            name=name,
            factory=factory
        )
