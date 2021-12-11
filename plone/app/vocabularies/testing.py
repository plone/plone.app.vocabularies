# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2


class PAVocabulariesLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.vocabularies
        self.loadZCML(
            package=plone.app.vocabularies,
            context=configurationContext
        )


PAVocabularies_FIXTURE = PAVocabulariesLayer()
PAVocabularies_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PAVocabularies_FIXTURE,),
    name='PAVocabularies:Integration',
)


class PAVocabulariesProtectedLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.vocabularies
        self.loadZCML(
            package=plone.app.vocabularies,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ["Member"])


PAVocabulariesProtected_FIXTURE = PAVocabulariesProtectedLayer()
PAVocabularies_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PAVocabulariesProtected_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PloneAppVocabularyProctedVocabularyLayer:Functional",
)
