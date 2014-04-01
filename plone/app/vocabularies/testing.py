from Products.CMFPlone.utils import getFSVersionTuple
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

PLONE5 = getFSVersionTuple()[0] >= 5


class PAVocabulariesLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.vocabularies
        self.loadZCML(
            package=plone.app.vocabularies,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        if not PLONE5:
            self.applyProfile(portal, 'plone.app.event:default')
            set_timezone(tz='UTC')


PAVocabularies_FIXTURE = PAVocabulariesLayer()
PAVocabularies_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PAVocabularies_FIXTURE,),
    name="PAVocabularies:Integration")
