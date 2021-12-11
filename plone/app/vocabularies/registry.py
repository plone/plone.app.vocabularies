from AccessControl import getSecurityManager
from zExceptions import Unauthorized
from zope.component.hooks import getSite

"""
TODO make vocabulary overwritable
TODO decorator for vocabulary factory (class), not just vocabulary component (function)
TODO No decorator, but zcml registration (> overwrite vocabulary)
"""

PERMISSION_ACCESS_ALL_VOCABULARIES = "View"

# My favorite line of code
all_vocabularies = {}


def _check_permission(permission=None, context=None):
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


# decorator implementation
def vocabulary(name, permission=None):
    """Register vocabulary with name.

    Vocabularies registered with permission
    are protected by permission in context.

    TODO TOBEDISCUSSED Is the __call__ method of
    the vocabulary factory (class),
    respectively the vocabulary component (function), to be protected
    or as we do here: is the vocabulary registration to be done
    with permission protection
    """
    def inner_decorator(f):
        if name:
            all_vocabularies[name] = {
                "component": f,
                "permission": permission
            }
        return f
    return inner_decorator


def queryVocabulary(name=None, context=None):
    """Get vocabulary of name 'name' or get list of vocabularies."""
    if name:
        # fetch permission of vocabulary registration
        permission = all_vocabularies.get(name, {}).get('permission', None)
        if permission:
            if _check_permission(permission, context):
                return all_vocabularies.get(name, {}).get('component', None)
            else:
                raise Unauthorized
        else:
            return all_vocabularies.get(name, {}).get('component', None)
    else:
        # return list of all vocabularies
        permission = PERMISSION_ACCESS_ALL_VOCABULARIES
        if _check_permission(permission=permission):
            return sorted(list(all_vocabularies.keys()))
