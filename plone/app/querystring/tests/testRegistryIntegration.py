from .base import QuerystringTestCase, TestProfileLayer, ptc


class TestOperationDefinitions(ptc.PloneTestCase):

    layer = TestProfileLayer

    def test_string_equality(self):
        registry = self.portal.portal_registry

        prefix = "plone.app.querystring.operation.string.is"
        self.assertTrue(prefix + '.title' in registry)

        self.assertEqual(registry[prefix + ".title"], "Is")
        self.assertEqual(registry[prefix + ".description"],
                         'Tip: you can use * to autocomplete.')
        self.assertEqual(registry[prefix + ".operation"],
                         'plone.app.querystring.queryparser:_equal')

    def test_date_lessthan(self):
        registry = self.portal.portal_registry
        prefix = 'plone.app.querystring.operation.date.lessThan'

        self.assertTrue(prefix + ".title" in registry)

        self.assertEqual(registry[prefix + ".title"], "Before date")
        self.assertEqual(registry[prefix + ".description"],
                         'Please use YYYY/MM/DD.')
        self.assertEqual(registry[prefix + ".operation"],
                         'plone.app.querystring.queryparser:_lessThan')


class TestFieldDefinitions(QuerystringTestCase):

    layer = TestProfileLayer

    def test_getId(self):
        registry = self.portal.portal_registry
        prefix = 'plone.app.querystring.field.getId'
        self.assertTrue(prefix + ".title" in registry)

        self.assertEqual(registry[prefix + ".title"], "Short name (id)")

        operations = registry[prefix + ".operations"]
        self.assertEqual(len(operations), 1)

        equal = 'plone.app.querystring.operation.string.is'
        self.assertTrue(equal in operations)

        self.assertEqual(registry[prefix + ".description"],
                         "The short name of an item (used in the url)")
        self.assertEqual(registry[prefix + ".enabled"], True)
        self.assertEqual(registry[prefix + ".sortable"], True)
        self.assertEqual(registry[prefix + ".group"], "Metadata")
