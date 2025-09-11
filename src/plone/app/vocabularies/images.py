from plone.namedfile.interfaces import IAvailableSizes
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


PMF = MessageFactory("plone")


@provider(IVocabularyFactory)
def ScalesVocabulary(context):
    """Obtains available scales from registry"""
    terms = []
    available_sizes = getUtility(IAvailableSizes)()
    if available_sizes is not None:
        for scale, (width, height) in available_sizes.items():
            translated = PMF(
                f"imagescale_{scale:s}",
                default=f"{scale:s} ${{width}}x${{height}}",
                mapping={"width": str(width), "height": str(height)},
            )
            terms.append(SimpleTerm(scale, scale, translated))
    return SimpleVocabulary(terms)
