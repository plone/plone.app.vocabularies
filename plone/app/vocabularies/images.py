# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import getAllowedSizes
from zope.i18nmessageid import MessageFactory
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import six


PMF = MessageFactory("plone")


@provider(IVocabularyFactory)
def ScalesVocabulary(context):
    """Obtains available scales from registry"""
    terms = []
    allowedSizes = getAllowedSizes()
    if allowedSizes is not None:
        for scale, (width, height) in six.iteritems(getAllowedSizes()):
            translated = PMF(
                "imagescale_{0:s}".format(scale),
                default="{0:s} ${{width}}x${{height}}".format(scale),
                mapping={"width": str(width), "height": str(height)},
            )
            terms.append(SimpleTerm(scale, scale, translated))
    return SimpleVocabulary(terms)
