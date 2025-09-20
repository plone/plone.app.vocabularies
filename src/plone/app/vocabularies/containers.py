from plone.base.navigationroot import get_navigation_root
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class RestoreContainersVocabulary:
    """Vocabulary of containers (folders) available for restoring recycled items.
    
    This vocabulary provides a list of all folders in the site that can be used
    as target containers when restoring items from the recycle bin.
    """
    
    def __call__(self, context):
        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')
        
        # Build vocabulary with site root first
        terms = []
        
        # Add site root as first option
        site_path = '/'.join(site.getPhysicalPath())
        terms.append(SimpleTerm(
            value=site_path,
            token=site_path,
            title="/ (Site Root)"
        ))
        
        # Query catalog for all folders
        query = {
            'is_folderish': True,
            'path': {'query': get_navigation_root(context)},
            'sort_on': 'sortable_title',
        }
        
        brains = catalog.searchResults(**query)
            
        for brain in brains:
            path = brain.getPath()
                
            # Skip the site root (already added)
            if path == site_path:
                continue
                    
           # Build a nice display title showing the path structure
            path_parts = path.split('/')
            site_parts = site_path.split('/')
                
            # Get relative path from site root
            if len(path_parts) > len(site_parts):
                relative_parts = path_parts[len(site_parts):]
                display_path = '/' + '/'.join(relative_parts)
            else:
                display_path = path
                    
            # Use brain title if available, otherwise use ID
            title = getattr(brain, 'Title', '') or brain.getId
            display_title = f"{display_path} ({title})"
                
            terms.append(SimpleTerm(
                value=path,
                token=path,
                title=display_title
            ))
            
        return SimpleVocabulary(terms)


RestoreContainersVocabularyFactory = RestoreContainersVocabulary()
