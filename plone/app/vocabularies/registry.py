from AccessControl import getSecurityManager
from zExceptions import Unauthorized
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface

"""
TODO make vocabulary overwritable
TODO handle vocabulary factory (class), not just vocabulary component (fct)
TODO No decorator, but zcml registration (> overwrite vocabulary)
"""

PERMISSION_ACCESS_ALL_VOCABULARIES = "View"


class IVocabularyRegistry(Interface):

    def queryVocabulary(self, name=None, context=None):
        """Get vocabulary of name 'name' or get list of vocabularies."""

    def registerVocabulary(self, name, f, permission=None):
        """Register vocabulary with name.

        permission is optional
        """


@implementer(IVocabularyRegistry)
class VocabularyRegistry():

    all_vocabularies = {}

    def _check_permission(self, permission=None, context=None):
        if not context:
            context = getSite()
        if not permission:
            return True
        sm = getSecurityManager()
        if not sm.checkPermission(permission, context):
            raise Unauthorized(
                f"Missing '{permission}' permission in context {context}"
            )
        return True

    def queryVocabulary(self, name=None, context=None):
        """Get vocabulary of name 'name' or get list of vocabularies."""
        if name:
            # fetch permission of vocabulary registration
            permission = self.all_vocabularies.get(
                name, {}).get(
                    'permission', None)
            if permission:
                if self._check_permission(permission, context):
                    return self.all_vocabularies.get(
                        name, {}).get(
                            'factory', None)
                else:
                    raise Unauthorized
            else:
                return self.all_vocabularies.get(name, {}).get('factory', None)
        else:
            # return list of all vocabularies
            permission = PERMISSION_ACCESS_ALL_VOCABULARIES
            if self._check_permission(permission=permission):
                return sorted(list(self.all_vocabularies.keys()))

    def registerVocabulary(self, name, factory, permission=None):
        """Register vocabulary with name.

        permission is optional
        """
        if name:
            self.all_vocabularies[name] = {
                "factory": factory,
                "permission": permission
            }
        else:
            raise ValueError("Please register vocabulary with name")
