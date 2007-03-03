from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName


class WorkflowStatesVocabulary(object):
    """Vocabulary factory for workflow states.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        wtool = getToolByName(context, 'portal_workflow')
        items = wtool.listWFStatesByTitle(filter_similar=True)
        item_dict = dict([(i[1], i[0]) for i in items])
        return SimpleVocabulary.fromItems([(item_dict[k], k) for k in sorted(item_dict.keys())])

WorkflowStatesVocabularyFactory = WorkflowStatesVocabulary()


class WorkflowTransitionsVocabulary(object):
    """Vocabulary factory for workflow transitions
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context):
        context = getattr(context, 'context', context)
        wtool = getToolByName(context, 'portal_workflow')
        
        transitions = []
        dup_list = {}
        for wf in wtool.objectValues():
            transition_folder = getattr(wf, 'transitions', None)
            if transition_folder is not None:
                for transition in transition_folder.objectValues():
                    key = '%s:%s' % (transition.id, transition.title,)
                    if not dup_list.has_key(key):
                        transitions.append(transition)
                    dup_list[key] = True
        items = [(s.title, s.getId()) for s in transitions]
        items.sort()
        return SimpleVocabulary.fromItems(items)

WorkflowTransitionsVocabularyFactory = WorkflowTransitionsVocabulary()
