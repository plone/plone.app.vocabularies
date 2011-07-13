from collective.testcaselayer import common
from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer.layer import Layer as BaseLayer
from plone.registry import Registry
from plone.registry.interfaces import IRegistry
from Products.PloneTestCase import PloneTestCase as ptc
from Testing import ZopeTestCase as ztc
from zope.component import getGlobalSiteManager


class RegistryLayer(BaseLayer):
    """A unittest layer that provides a new plone.registry."""

    def setUp(self):
        gsm = getGlobalSiteManager()
        self.registry = Registry()
        gsm.registerUtility(self.registry, IRegistry)

    def tearDown(self):
        gsm = getGlobalSiteManager()
        gsm.unregisterUtility(provided=IRegistry)


class QuerystringInstalled(tcl_ptc.BasePTCLayer):
    """A PloneTestCase layer that loads the ZCML for plone.app.querystring and
       installs the package into zope.
    """

    def afterSetUp(self):
        import plone.app.querystring
        self.loadZCML('configure.zcml', package=plone.app.querystring)
        ztc.installPackage('plone.app.querystring')


class RealGSProfile(tcl_ptc.PTCLayer):
    """A PloneTestCase layer that runs the plone.app.querystring GenericSetup
       profile.
    """

    def afterSetUp(self):
        self.addProfile('plone.app.querystring:default')


class TestGSProfile(tcl_ptc.PTCLayer):
    """A PloneTestCase layer that runs a GenericSetup profile containing test
       data.
    """

    def afterSetUp(self):
        import plone.app.querystring.tests
        self.loadZCML('configure.zcml', package=plone.app.querystring.tests)
        self.addProfile('plone.app.querystring.tests:registry')

# The layers available to test authors

UnittestLayer = BaseLayer([], name="UnittestLayer")
UnittestWithRegistryLayer = RegistryLayer([UnittestLayer, ])
UninstalledLayer = tcl_ptc.BasePTCLayer([common.common_layer, ])
InstalledLayer = QuerystringInstalled([UninstalledLayer, ])
TestProfileLayer = TestGSProfile([InstalledLayer, ])
FullProfilelayer = RealGSProfile([InstalledLayer, ])


class QuerystringTestCase(ptc.PloneTestCase):
    layer = FullProfilelayer


class QuerystringFunctionalTestCase(ptc.FunctionalTestCase,
                                    QuerystringTestCase):
    pass
