# -*- coding: utf-8 -*-
from plone.app.vocabularies.interfaces import ISlicableVocabulary
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


GETTER = {'user': 'getUserById', 'group': 'getGroupById'}

SOURCES = {
    'user': {
        'search': 'searchUsers',
        'searchargs': {'sort_by': 'title'},
        'get': 'getUserById',
        'prefix': False,
        'many': ['plone.many_users'],
    },
    'group': {
        'search': 'searchGroups',
        'searchargs': {'sort_by': 'title'},
        'get': 'getGroupById',
        'prefix': False,
        'many': ['plone.many_groups'],
    },
    'principal': {
        'search': 'searchPrincipals',
        'searchargs': {'sort_by': 'title', 'groups_first': True},
        'get': 'getPrincipalById',
        'prefix': True,
        'many': ['plone.many_users', 'plone.many_groups'],
    },
}


@implementer(ISlicableVocabulary)
class PrincipalsVocabulary(SimpleVocabulary):
    """Vocabulary dealing with users/ groups (or in theory any other principal)
    """

    @property
    def principal_source(self):
        return self._principal_source

    @principal_source.setter
    def principal_source(self, value):
        self._principal_source = value

    @property
    def _acl_users(self):
        aclu = getattr(self, "_aclu", None)
        if not aclu:
            aclu = self._aclu = getToolByName(getSite(), 'acl_users')
        return aclu

    def __contains__(self, value):
        """Checks if the principal exists in PAS, not only in the queried subset
        """
        if SOURCES[self._principal_source]['prefix']:
            principal_type, principal_id = value.split(':', 2)
        else:
            principal_type = self._principal_source
            principal_id = value
        getter = getattr(self._acl_users, GETTER[principal_type])
        return bool(getter(principal_id, None))

    def __getitem__(self, start, stop=None):
        """Sliceable"""
        if isinstance(start, slice):
            slice_inst = start
            start = slice_inst.start
            stop = slice_inst.stop
        elif not stop:
            return self._terms[start]

        # sliced up
        return self._terms[start:stop]


class BaseFactory(object):
    """Factory creating a PrincipalsVocabulary
    """

    def should_search(self, query):
        ''' Test if we should search for users
        '''
        if query:
            return True
        registry = getUtility(IRegistry)
        return not [
            x for x in filter(registry.get, SOURCES[self.source]["many"])
        ]

    def use_principal_triple(self, principal_triple):
        """Used by ``functools.filter`` to decide if the triple should be used.

        principal_triple
            A triple (token, value, title).
            Like (johndoe, johndoe, 'John Doe') (unprefixed).
            Value might be a prefixed Id by principal_type, like
            (user__johndoe, user:johndoe, 'John Doe') or
            (group__editors, group:editors, 'Editors').

        Meant to be overriden in subclasses.
        """
        return True

    def __call__(self, context, query=''):
        if not self.should_search(query):
            return PrincipalsVocabulary.fromItems([])
        acl_users = getToolByName(context, 'acl_users')
        search = getattr(acl_users, SOURCES[self.source]['search'])

        def principal_triples():
            # TODO: fullname ok here?
            for info in search(
                fullname=query, **SOURCES[self.source]['searchargs']
            ):
                principal_id = info['id']
                if SOURCES[self.source]['prefix']:
                    principal_id = "{0}:{1}".format(
                        info['principal_type'], principal_id
                    )
                principal_token = principal_id.replace(':', '__')
                yield (principal_token, principal_id, info['title'])

        filtered_principal_triples = filter(
            self.use_principal_triple, principal_triples()
        )
        vocabulary = PrincipalsVocabulary.fromItems(filtered_principal_triples)
        vocabulary.principal_source = self.source
        return vocabulary


@implementer(IVocabularyFactory)
class PrincipalsFactory(BaseFactory):
    source = 'principal'


@implementer(IVocabularyFactory)
class UsersFactory(BaseFactory):
    source = 'user'


@implementer(IVocabularyFactory)
class GroupsFactory(BaseFactory):
    source = 'group'
