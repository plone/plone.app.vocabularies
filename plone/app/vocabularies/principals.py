# -*- coding: utf-8 -*-
from plone.app.vocabularies.interfaces import ISlicableVocabulary
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


GETTER = {'user': 'getUserById', 'group': 'getGroupById'}

_USER_SEARCH = {
    'search': 'searchUsers',
    # Hint: The fullname search is provided i.e. in IUserEnumeration of
    # the property plugin in PlonePAS.
    'searchattr': 'fullname',
    'searchargs': {'sort_by': 'fullname'},
    'many': 'plone.many_users',
}
_GROUP_SEARCH = {
    'search': 'searchGroups',
    # Hint: The fullname search is excluded in i.e. in IUserEnumeration of
    # the property plugin in PlonePAS. title  is supported.
    'searchattr': 'title',
    'searchargs': {'sort_by': 'title'},
    'many': 'plone.many_groups',
}

SOURCES = {
    'user': {
        'searches': [_USER_SEARCH],
        'get': 'getUserById',
        'prefix': False,
    },
    'group': {
        'searches': [_GROUP_SEARCH],
        'get': 'getGroupById',
        'prefix': False,
    },
    'principal': {
        'searches': [_GROUP_SEARCH, _USER_SEARCH],
        'get': 'getPrincipalById',
        'prefix': True,
    },
}


def _get_acl_users():
    return getToolByName(getSite(), 'acl_users')


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
        aclu = getattr(self, '_aclu', None)
        if not aclu:
            aclu = self._aclu = _get_acl_users()
        return aclu

    def _get_from_source(self, value, default=None):
        """Helper to get a user or group from users folder.
        """
        if SOURCES[self._principal_source]['prefix']:
            if ':' not in value:
                return default
            principal_type, principal_id = value.split(':', 2)
        else:
            principal_type = self._principal_source
            principal_id = value
        getter = getattr(self._acl_users, GETTER[principal_type])
        return getter(principal_id, default)

    def __contains__(self, value):
        """Checks if the principal exists in current subset or in PAS.
        """
        result = super(PrincipalsVocabulary, self).__contains__(value)
        return result or bool(self._get_from_source(value))

    def getTerm(self, value):
        """Checks also for values not in the current subset.
        This allows to lookup already saved values.
        """
        try:
            return super(PrincipalsVocabulary, self).getTerm(value)
        except LookupError:
            user = self._get_from_source(value)
            if user is None:
                raise
            if user.isGroup():
                title = user.getProperty('title', value) or value
            else:
                title = user.getProperty('fullname', value) or value
            if SOURCES[self._principal_source]['prefix']:
                token = value.replace(':', '__', 1)
            else:
                token = value
            return self.__class__.createTerm(value, token, title)

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

    source = None

    def should_search(self, query):
        """ Test if we should search for users
        """
        if query:
            return True
        registry = getUtility(IRegistry)
        return not [
            x
            for x in filter(
                registry.get,
                [cfg['many'] for cfg in SOURCES[self.source]['searches']],
            )
        ]

    def use_principal_triple(self, principal_triple):
        """Used by ``functools.filter`` to decide if the triple should be used.

        principal_triple
            A triple (token, value, title).
            Like (johndoe, johndoe, 'John Doe') (unprefixed).
            Value might be a prefixed Id by principal_type, like
            (user__johndoe, user:johndoe, 'John Doe') or
            (group__editors, group:editors, 'Editors').

        returns wether the triple shall be included in the vocabulary or not
        (bool).

        Meant to be overriden in subclasses for post-filtering result.
        """
        return True

    def __call__(self, context, query=''):
        if not self.should_search(query):
            vocabulary = PrincipalsVocabulary([])
            vocabulary.principal_source = self.source
            return vocabulary
        acl_users = _get_acl_users()
        cfg = SOURCES[self.source]

        def principal_triples():
            for search_cfg in cfg['searches']:
                search = getattr(acl_users, search_cfg['search'])
                searchargs = search_cfg['searchargs'].copy()
                searchargs[search_cfg['searchattr']] = query
                for info in search(**searchargs):
                    principal_id = info['id']
                    if cfg['prefix']:
                        principal_id = '{0}:{1}'.format(
                            info['principal_type'], principal_id
                        )
                    principal_token = principal_id.replace(':', '__')
                    yield (principal_token, principal_id, info['title'])

        filtered_principal_triples = filter(
            self.use_principal_triple, principal_triples()
        )
        terms = [SimpleTerm(token, id_, title) for
                 (token, id_, title) in filtered_principal_triples]
        vocabulary = PrincipalsVocabulary(terms)
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
