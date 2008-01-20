from Acquisition import Explicit

class DummyContext(Explicit):

    def __init__(self):
        self.context = None

class DummyTool(Explicit):

    def __init__(self, name):
        self.name = name
