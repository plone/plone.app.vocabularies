# -*- coding: utf-8 -*-
from plone.app.imaging.utils import getAllowedSizes
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import provider


@provider(IVocabularyFactory)
def ScalesVocabulary(context):
    """Obtains available scales from plone.app.imaging
    """
    terms = []
    for scale, (width, height) in getAllowedSizes().iteritems():
        terms.append(SimpleTerm(scale, scale, "{:s} {:d}x{:d}".format (
            scale, width, height)))

    return SimpleVocabulary(terms)
