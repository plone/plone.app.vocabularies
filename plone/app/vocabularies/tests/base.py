from Acquisition import Explicit

class DummyContext(Explicit):

    def __init__(self):
        self.context = None


class DummyTool(Explicit):

    def __init__(self, name):
        self.name = name


class DummyType(object):

    def __init__(self, title):
        self.title = title

    def Title(self):
        return self.title


class DummyTypeTool(dict):

    def __init__(self):
        self['Document'] = DummyType('Page')
        self['Event'] = DummyType('Event')

    def listContentTypes(self):
        return self.keys()
