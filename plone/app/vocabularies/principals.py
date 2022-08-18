from plone.app.vocabularies.interfaces import ISlicableVocabulary
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


GETTER = {"user": "getUserById", "group": "getGroupById"}

_USER_SEARCH = {
    "search": "searchUsers",
    # Hint: The fullname search is provided i.e. in IUserEnumeration of
    # the property plugin in PlonePAS.
    "searchattr": "fullname",
    "searchargs": {"sort_by": "fullname"},
    "many": "plone.many_users",
}
_GROUP_SEARCH = {
    "search": "searchGroups",
    # Hint: The fullname search is excluded in i.e. in IUserEnumeration of
    # the property plugin in PlonePAS. title is supported.
    "searchattr": "title",
    "searchargs": {"sort_by": "title"},
    "many": "plone.many_groups",
}

SOURCES = {
    "user": {
        "searches": [_USER_SEARCH],
        "get": "getUserById",
        "prefix": False,
    },
    "group": {
        "searches": [_GROUP_SEARCH],
        "get": "getGroupById",
        "prefix": False,
    },
    "principal": {
        "searches": [_GROUP_SEARCH, _USER_SEARCH],
        "get": "getPrincipalById",
        "prefix": True,
    },
}


def token_from_principal_info(info, prefix=False):
    # we assume the id is always ready to be consumed as a token, either
    # for patternlib or for options tag (where the standard wants
    # something CDATA compatible)
    if not prefix:
        return info["id"]
    # we use a double underscore here, a colon is already used in pattern
    # values as separator
    return "{}__{}".format(info["principal_type"], info["id"])


def merge_principal_infos(infos, prefix=False):
    info = infos[0]
    if len(infos) > 1:
        principal_types = {
            info["principal_type"] for info in infos if info["principal_type"]
        }
        if len(principal_types) > 1:
            # Principals with the same ID but different types. Should not
            # happen.
            raise ValueError("Principal ID not unique: {}".format(info["id"]))
        if not info["title"]:
            for candidate in infos:
                if candidate["title"]:
                    info["title"] = candidate["title"]
                    break
    return info


def _get_acl_users():
    return getToolByName(getSite(), "acl_users")


@implementer(ISlicableVocabulary)
class PrincipalsVocabulary(SimpleVocabulary):
    """Vocabulary dealing with users/ groups (or in theory any other principal)"""

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
            aclu = self._aclu = _get_acl_users()
        return aclu

    def _get_principal_from_source(self, value=None, token=None, default=None):
        """Helper to get a user or group from users folder."""
        if not (bool(value) ^ bool(token)):  # not (value xor token)
            raise ValueError("value or token must be provided (only one of those)")
        if SOURCES[self._principal_source]["prefix"]:
            if value:
                if ":" not in value:
                    return default
                principal_type, principal_id = value.split(":", 2)
            else:
                if "__" not in token:
                    return default
                principal_type, principal_id = token.split("__", 2)
        else:
            principal_type = self._principal_source
            principal_id = value or token
        getter = getattr(self._acl_users, GETTER[principal_type])
        return getter(principal_id, default)

    def _get_term_from_source(self, value=None, token=None):
        """Helper to get a user or group from users folder."""
        if not (bool(value) ^ bool(token)):  # not (value xor token)
            raise ValueError("value or token must be provided (only one of those)")
        principal = self._get_principal_from_source(value=value, token=token)
        if principal is None:
            raise LookupError(f"Principal {value or token} not found")
        if principal.isGroup():
            title = principal.getProperty("title", principal.getId())
            principal_type = "group"
        else:
            title = principal.getProperty("fullname", principal.getId())
            principal_type = "user"
        if token:
            value = principal.getId()
            if SOURCES[self._principal_source]["prefix"]:
                value = f"{principal_type}:{value}"
        else:
            token = principal.getId()
            if SOURCES[self._principal_source]["prefix"]:
                token = f"{principal_type}__{token}"
        return self.__class__.createTerm(value, token, title)

    def __contains__(self, value):
        """Checks if the principal exists in current subset or in PAS."""
        result = super().__contains__(value)
        return result or bool(self._get_principal_from_source(value=value))

    def getTerm(self, value):
        """Checks also for values not in the current subset.
        This allows to lookup already saved values.
        """
        try:
            return super().getTerm(value)
        except LookupError:
            return self._get_term_from_source(value=value)

    def getTermByToken(self, token):
        """Checks also for tokens not in the current subset.
        This allows to lookup already saved values by token.
        """
        try:
            return super().getTermByToken(token)
        except LookupError:
            return self._get_term_from_source(token=token)

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


class BaseFactory:
    """Factory creating a PrincipalsVocabulary"""

    source = None

    def should_search(self, query):
        """Test if we should search for users"""
        if query:
            return True
        registry = getUtility(IRegistry)
        return not [
            x
            for x in filter(
                registry.get,
                [cfg["many"] for cfg in SOURCES[self.source]["searches"]],
            )
        ]

    def use_principal_triple(self, principal_triple):
        """Used by ``functools.filter`` to decide if the triple should be used.

        principal_triple
            A triple (value, token, title).
            Like (johndoe, johndoe, 'John Doe') (unprefixed).
            Value might be a prefixed Id by principal_type, like
            (user:johndoe, user__johndoe, 'John Doe') or
            (group:editors, group__editors, 'Editors').

        returns wether the triple shall be included in the vocabulary or not
        (bool).

        Meant to be overriden in subclasses for post-filtering result.
        """
        return True

    def __call__(self, context, query=""):
        if not self.should_search(query):
            vocabulary = PrincipalsVocabulary([])
            vocabulary.principal_source = self.source
            return vocabulary
        acl_users = _get_acl_users()
        cfg = SOURCES[self.source]

        def term_triples():
            """Generator for term triples (value, token, name)"""
            for search_cfg in cfg["searches"]:
                search = getattr(acl_users, search_cfg["search"])
                searchargs = search_cfg["searchargs"].copy()
                searchargs[search_cfg["searchattr"]] = query
                infotree = {}
                for info in search(**searchargs):
                    infotree.setdefault(info["id"], {}).setdefault(
                        info["principal_type"], []
                    ).append(info)
                for principal_id, types_infos in infotree.items():
                    if len(types_infos) > 1 and not cfg["prefix"]:
                        raise ValueError(f"Principal ID not unique: {principal_id}")
                    for principal_type, principal_infos in types_infos.items():
                        value = principal_id
                        info = merge_principal_infos(principal_infos)
                        if cfg["prefix"]:
                            value = "{}:{}".format(info["principal_type"], value)
                        token = token_from_principal_info(info, prefix=cfg["prefix"])
                        yield (value, token, info["title"])

        vocabulary = PrincipalsVocabulary(
            [
                SimpleTerm(*term_triple)
                for term_triple in filter(self.use_principal_triple, term_triples())
            ]
        )
        vocabulary.principal_source = self.source
        return vocabulary


@implementer(IVocabularyFactory)
class PrincipalsFactory(BaseFactory):
    source = "principal"


@implementer(IVocabularyFactory)
class UsersFactory(BaseFactory):
    source = "user"


@implementer(IVocabularyFactory)
class GroupsFactory(BaseFactory):
    source = "group"
