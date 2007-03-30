from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.interfaces import ISkinsTool
from Products.CMFPlone import PloneMessageFactory as _

class SkinsVocabularyFactory(object):
    """Vocabulary factory for skins.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        stool = getUtility(ISkinsTool)
        items = [ (s, s)
                  for s in stool.getSkinSelections() ]
        items.sort()
        return SimpleVocabulary.fromItems(items)

SkinsVocabularyFactory = SkinsVocabularyFactory()

class IconVisibilityFactory(object):
    """Vocabulary factory for icon visiblity.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        vd = {
            _(u"Only for users who are logged in"): 'authenticated',
            _(u"Never show icons"): 'disabled',
            _(u"Always show icons"): 'enabled',}
        return SimpleVocabulary.fromItems(vd.items())

IconVisibilityFactory = IconVisibilityFactory()
