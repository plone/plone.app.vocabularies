from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate

from Products.CMFCore.utils import getToolByName
_ = MessageFactory('plone')

class WorkflowsVocabulary(object):
    """Vocabulary factory for workflows.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        wtool = getToolByName(context, 'portal_workflow')
        items = [(w.title, w.id) for w in wtool.objectValues()]
        items.sort()
        return SimpleVocabulary.fromItems(items)

WorkflowsVocabularyFactory = WorkflowsVocabulary()

class WorkflowStatesVocabulary(object):
    """Vocabulary factory for workflow states.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        wtool = getToolByName(context, 'portal_workflow')
        items = wtool.listWFStatesByTitle(filter_similar=True)
        items_dict = dict([(i[1], translate(_(i[0]), context=context)) for i in items])
        items_list = [(k, v) for k, v in items_dict.items()]
        items_list.sort(lambda x, y: cmp(x[1], y[1]))
        terms = [SimpleTerm(k, title=u'%s [%s]' % (v, k)) for k, v in items_list]
        return SimpleVocabulary(terms)

WorkflowStatesVocabularyFactory = WorkflowStatesVocabulary()


class WorkflowTransitionsVocabulary(object):
    """Vocabulary factory for workflow transitions
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        wtool = getToolByName(context, 'portal_workflow')

        transitions = {}

        for wf in wtool.objectValues():
            transition_folder = getattr(wf, 'transitions', None)
            wf_name = wf.title or wf.id
            if transition_folder is not None:
                for transition in transition_folder.objectValues():
                    transition_title = transition.actbox_name
                    transitions.setdefault(transition.id, []).append(dict(title=transition_title,
                                                                        wf_name=wf_name))
        items = []
        for transition_id, info in transitions.items():
            titles = set([i['title'] for i in info])
            item_title = ' // '.join(sorted(titles))
            items.append(("%s [%s]" % (item_title, transition_id,), transition_id),)

        return SimpleVocabulary.fromItems(sorted(items))

WorkflowTransitionsVocabularyFactory = WorkflowTransitionsVocabulary()
