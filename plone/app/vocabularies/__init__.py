from zope.interface import implements
from zope.interface import directlyProvides
from plone.app.vocabularies.interfaces import ISlicableVocabulary


class SlicableVocabulary(object):
    """
    A tokenized voacabulary in which the results can be sliced.
    """
    implements(ISlicableVocabulary)

    def __init__(self, terms=[], *interfaces):
        self._terms = terms
        if interfaces:
            directlyProvides(self, *interfaces)

    def __getitem__(self, start, stop=None):
        if isinstance(start, slice):
            slic = start
            start = slic.start
            stop = slic.stop
        elif not stop:
            return self._terms[start]

        # sliced up
        results = []
        for item in self._terms[start:stop]:
            results.append(self.getTerm(item))
        return results

    def __len__(self):
        return len(self._terms)
