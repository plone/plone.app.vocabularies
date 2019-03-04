# -*- coding: utf-8 -*-
from plone.app.vocabularies.testing import PAVocabularies_INTEGRATION_TESTING
import unittest


class PrincipalsTest(unittest.TestCase):
    layer = PAVocabularies_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def _make_user(self, userid, fullname):
        user = self.portal['acl_users']._doAddUser(
            userid, 'secret', ['Member'], []
        )
        user.setProperties(fullname=fullname)

    def _make_group(self, groupid, title):
        self.portal['acl_users']._doAddGroup(groupid, [], title=title)

    def test_empty_principals_vocabulary(self):
        from plone.app.vocabularies.principals import PrincipalsVocabulary

        vocab = PrincipalsVocabulary([])
        vocab.principal_source = 'user'

        # basic data
        self.assertEqual(vocab.principal_source, 'user')
        self.assertEqual(vocab._acl_users, self.portal['acl_users'])

    def test_pas_connectivity_user(self):
        self._make_user('user1', 'User One')

        from plone.app.vocabularies.principals import PrincipalsVocabulary

        vocab = PrincipalsVocabulary([])
        vocab.principal_source = 'user'

        # test 1
        vuser = vocab._get_from_source('user1')
        self.assertEqual(vuser.getId(), 'user1')

        # test 2
        term = vocab.getTerm('user1')
        self.assertEqual(term.value, 'user1')
        self.assertEqual(term.token, 'user1')
        self.assertEqual(term.title, 'User One')
        with self.assertRaises(LookupError):
            term = vocab.getTerm('user:non-existing')
        with self.assertRaises(LookupError):
            term = vocab.getTerm('non-existing')

    def test_pas_connectivity_group(self):
        self._make_group('group1', 'Group One')

        from plone.app.vocabularies.principals import PrincipalsVocabulary

        vocab = PrincipalsVocabulary([])
        vocab.principal_source = 'group'

        # test 1
        vgroup = vocab._get_from_source('group1')
        self.assertEqual(vgroup.getId(), 'group1')

        # test 2
        term = vocab.getTerm('group1')
        self.assertEqual(term.value, 'group1')
        self.assertEqual(term.token, 'group1')
        self.assertEqual(term.title, 'Group One')
        with self.assertRaises(LookupError):
            term = vocab.getTerm('group:non-existing')
        with self.assertRaises(LookupError):
            term = vocab.getTerm('non-existing')

    def test_pas_connectivity_principal(self):
        self._make_user('user1', 'User One')
        self._make_group('group1', 'Group One')

        from plone.app.vocabularies.principals import PrincipalsVocabulary

        vocab = PrincipalsVocabulary([])
        vocab.principal_source = 'principal'

        # test 1
        vgroup = vocab._get_from_source('user:user1')
        self.assertEqual(vgroup.getId(), 'user1')
        vgroup = vocab._get_from_source('group:group1')
        self.assertEqual(vgroup.getId(), 'group1')

        # test 2
        term = vocab.getTerm('user:user1')
        self.assertEqual(term.value, 'user:user1')
        self.assertEqual(term.token, 'user__user1')
        self.assertEqual(term.title, 'User One')
        term = vocab.getTerm('group:group1')
        self.assertEqual(term.value, 'group:group1')
        self.assertEqual(term.token, 'group__group1')
        self.assertEqual(term.title, 'Group One')
        with self.assertRaises(LookupError):
            term = vocab.getTerm('user:non-existing')
        with self.assertRaises(LookupError):
            term = vocab.getTerm('group:non-existing')
        with self.assertRaises(LookupError):
            term = vocab.getTerm('non-existing')

    def test_populated_user(self):
        from zope.schema.vocabulary import SimpleTerm

        terms = [
            SimpleTerm(
                'user_{0}'.format(idx),
                'user{0}'.format(idx),
                'User {0}'.format(idx),
            )
            for idx in range(0, 10)
        ]

        from plone.app.vocabularies.principals import PrincipalsVocabulary

        vocab = PrincipalsVocabulary(terms)
        vocab.principal_source = 'user'

        self.assertEqual(vocab.getTerm('user_3').value, 'user_3')
        self.assertEqual(vocab.getTerm('user_3').token, 'user3')
        self.assertEqual(vocab.getTerm('user_3').title, 'User 3')

        self.assertEqual(vocab.getTermByToken('user3').value, 'user_3')
        self.assertEqual(vocab.getTermByToken('user3').token, 'user3')
        self.assertEqual(vocab.getTermByToken('user3').title, 'User 3')

        self.assertEqual(vocab[6].value, 'user_6')
        self.assertEqual(
            ['user_2', 'user_3', 'user_4', 'user_5'],
            [term.value for term in vocab[2:6]],
        )

        self.assertTrue('user_2' in vocab)
        self.assertFalse('non-existing' in vocab)

    def test_populated_group(self):
        from zope.schema.vocabulary import SimpleTerm

        terms = [
            SimpleTerm(
                'group_{0}'.format(idx),
                'group{0}'.format(idx),
                'Group {0}'.format(idx),
            )
            for idx in range(0, 10)
        ]

        from plone.app.vocabularies.principals import PrincipalsVocabulary

        vocab = PrincipalsVocabulary(terms)
        vocab.principal_source = 'group'

        self.assertEqual(vocab.getTerm('group_3').value, 'group_3')
        self.assertEqual(vocab.getTerm('group_3').token, 'group3')
        self.assertEqual(vocab.getTerm('group_3').title, 'Group 3')

        self.assertEqual(vocab.getTermByToken('group3').value, 'group_3')
        self.assertEqual(vocab.getTermByToken('group3').token, 'group3')
        self.assertEqual(vocab.getTermByToken('group3').title, 'Group 3')

        self.assertEqual(vocab[6].value, 'group_6')
        self.assertEqual(
            ['group_2', 'group_3', 'group_4', 'group_5'],
            [term.value for term in vocab[2:6]],
        )

        self.assertTrue('group_2' in vocab)
        self.assertFalse('non-existing' in vocab)

    def test_populated_principals(self):
        from zope.schema.vocabulary import SimpleTerm

        terms = [
            SimpleTerm(
                'user:user_{0}'.format(idx),
                'user__user{0}'.format(idx),
                'User {0}'.format(idx),
            )
            for idx in range(0, 10)
        ]
        terms += [
            SimpleTerm(
                'group:group_{0}'.format(idx),
                'group__group{0}'.format(idx),
                'Group {0}'.format(idx),
            )
            for idx in range(0, 10)
        ]

        from plone.app.vocabularies.principals import PrincipalsVocabulary

        vocab = PrincipalsVocabulary(terms)
        vocab.principal_source = 'principal'

        # users
        self.assertEqual(vocab.getTerm('user:user_4').value, 'user:user_4')
        self.assertEqual(vocab.getTerm('user:user_3').token, 'user__user3')
        self.assertEqual(vocab.getTerm('user:user_6').title, 'User 6')

        self.assertEqual(
            vocab.getTermByToken('user__user4').value, 'user:user_4'
        )
        self.assertEqual(
            vocab.getTermByToken('user__user3').token, 'user__user3'
        )
        self.assertEqual(vocab.getTermByToken('user__user6').title, 'User 6')

        self.assertTrue('user:user_2' in vocab)
        self.assertFalse('non-existing' in vocab)

        # groups
        self.assertEqual(vocab.getTerm('group:group_3').value, 'group:group_3')
        self.assertEqual(vocab.getTerm('group:group_3').token, 'group__group3')
        self.assertEqual(vocab.getTerm('group:group_3').title, 'Group 3')

        self.assertEqual(
            vocab.getTermByToken('group__group3').value, 'group:group_3'
        )
        self.assertEqual(
            vocab.getTermByToken('group__group3').token, 'group__group3'
        )
        self.assertEqual(
            vocab.getTermByToken('group__group3').title, 'Group 3'
        )

        # getitem/slice
        self.assertEqual(vocab[6].value, 'user:user_6')
        self.assertEqual(
            ['group:group_7', 'group:group_8', 'group:group_9'],
            [term.value for term in vocab[17:]],
        )
        self.assertEqual(
            ['user:user_8', 'user:user_9', 'group:group_0'],
            [term.value for term in vocab[8:11]],
        )

        # contains
        self.assertTrue('group:group_2' in vocab)
        self.assertFalse('non-existing' in vocab)

    def test_factory_user_blank(self):
        for idx in range(0, 10):
            # creates user0: 'Abc User'; user1, 'Bcd User', ...
            userid = 'user{0}'.format(idx)
            fullname = chr(65 + idx) + chr(98 + idx) + chr(99 + idx) + ' User'
            self._make_user(userid, fullname)

        from plone.app.vocabularies.principals import UsersFactory

        factory = UsersFactory()
        vocab = factory(self.portal)
        self.assertEqual(vocab.getTerm('user0').title, 'Abc User')
        self.assertEqual(vocab.getTerm('user2').title, 'Cde User')

    def test_factory_user_query(self):
        for idx in range(0, 10):
            # creates user0: 'Abc User'; user1, 'Bcd User', ...
            userid = 'user{0}'.format(idx)
            fullname = chr(65 + idx) + chr(98 + idx) + chr(99 + idx) + ' User'
            self._make_user(userid, fullname)

        from plone.app.vocabularies.principals import UsersFactory

        factory = UsersFactory()
        vocab = factory(self.portal, query='Cde')

        # reduced by query
        self.assertEqual([term.value for term in vocab], ['user2'])

        # but getTerm still works for all
        self.assertEqual(vocab.getTerm('user0').title, 'Abc User')
        self.assertEqual(vocab.getTerm('user2').title, 'Cde User')

        # contains works too
        self.assertTrue('user0' in vocab)
        self.assertTrue('user2' in vocab)

    def test_factory_group_blank(self):
        for idx in range(0, 10):
            # creates group0: 'Abc Group'; group1, 'Bcd Group', ...
            groupid = 'group{0}'.format(idx)
            fullname = chr(65 + idx) + chr(98 + idx) + chr(99 + idx) + ' Group'
            self._make_group(groupid, fullname)

        from plone.app.vocabularies.principals import GroupsFactory

        factory = GroupsFactory()
        vocab = factory(self.portal)
        self.assertEqual(vocab.getTerm('group0').title, 'Abc Group')
        self.assertEqual(vocab.getTerm('group2').title, 'Cde Group')

    def test_factory_group_query(self):
        for idx in range(0, 10):
            # creates user0: 'Abc User'; user1, 'Bcd User', ...
            groupid = 'group{0}'.format(idx)
            fullname = chr(65 + idx) + chr(98 + idx) + chr(99 + idx) + ' Group'
            self._make_group(groupid, fullname)

        from plone.app.vocabularies.principals import GroupsFactory

        factory = GroupsFactory()
        vocab = factory(self.portal, query='Cde')

        # reduced by query
        self.assertEqual([term.value for term in vocab], ['group2'])

        # but getTerm still works for all
        self.assertEqual(vocab.getTerm('group0').title, 'Abc Group')
        self.assertEqual(vocab.getTerm('group2').title, 'Cde Group')

        # contains works too
        self.assertTrue('group0' in vocab)
        self.assertTrue('group2' in vocab)

    def test_factory_principal_blank(self):
        for idx in range(0, 10):
            # creates user0: 'Abc User'; user1, 'Bcd User', ...
            userid = 'user{0}'.format(idx)
            fullname = chr(65 + idx) + chr(98 + idx) + chr(99 + idx) + ' User'
            self._make_user(userid, fullname)
        for idx in range(0, 10):
            # creates group0: 'Abc Group'; group1, 'Bcd Group', ...
            groupid = 'group{0}'.format(idx)
            fullname = chr(65 + idx) + chr(98 + idx) + chr(99 + idx) + ' Group'
            self._make_group(groupid, fullname)

        from plone.app.vocabularies.principals import PrincipalsFactory

        factory = PrincipalsFactory()
        vocab = factory(self.portal)
        self.assertEqual(vocab.getTerm('user:user0').title, 'Abc User')
        self.assertEqual(vocab.getTerm('user:user2').title, 'Cde User')
        self.assertEqual(vocab.getTerm('group:group0').title, 'Abc Group')
        self.assertEqual(vocab.getTerm('group:group2').title, 'Cde Group')

    def test_factory_principal_query(self):
        for idx in range(0, 10):
            # creates user0: 'Abc User'; user1, 'Bcd User', ...
            userid = 'user{0}'.format(idx)
            fullname = chr(65 + idx) + chr(98 + idx) + chr(99 + idx) + ' User'
            self._make_user(userid, fullname)
        for idx in range(0, 10):
            # creates group0: 'Abc Group'; group1, 'Bcd Group', ...
            groupid = 'group{0}'.format(idx)
            fullname = chr(65 + idx) + chr(98 + idx) + chr(99 + idx) + ' Group'
            self._make_group(groupid, fullname)

        from plone.app.vocabularies.principals import PrincipalsFactory

        factory = PrincipalsFactory()
        vocab = factory(self.portal, query='Cde')

        # reduced by query
        self.assertEqual(
            [term.value for term in vocab], ['group:group2', 'user:user2']
        )

        # but getTerm still works for all
        self.assertEqual(vocab.getTerm('user:user0').title, 'Abc User')
        self.assertEqual(vocab.getTerm('user:user2').title, 'Cde User')
        self.assertEqual(vocab.getTerm('group:group0').title, 'Abc Group')
        self.assertEqual(vocab.getTerm('group:group2').title, 'Cde Group')

        # contains works too
        self.assertTrue('user:user0' in vocab)
        self.assertTrue('user:user2' in vocab)
        self.assertTrue('group:group0' in vocab)
        self.assertTrue('group:group2' in vocab)
