from Products.CMFPlone.utils import getAllowedSizes
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
    allowedSizes = getAllowedSizes()
    if allowedSizes is not None:
        for scale, (width, height) in getAllowedSizes().items():
            translated = PMF(
                f"imagescale_{scale:s}",
                default=f"{scale:s} ${{width}}x${{height}}",
                mapping={"width": str(width), "height": str(height)},
            )
            terms.append(SimpleTerm(scale, scale, translated))
    return SimpleVocabulary(terms)
