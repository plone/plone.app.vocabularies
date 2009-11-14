from Products.ZCTextIndex.ParseTree import ParseError


class DummyContext(object):

    def __init__(self):
        self.context = None


class DummyTool(object):

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


class Response(dict):

    def getHeader(self, value):
        return 'header %s' % value


class Request(dict):

    debug = False
    response = Response()

    def __init__(self, form=None):
        self.form = form


class Brain(object):

    Title = 'BrainTitle'
    is_folderish = True

    def __init__(self, rid):
        self.rid = rid

    def getPath(self):
        return self.rid


class DummyCatalog(dict):

    def __init__(self, values):
        for r in values:
            self[r] = Brain(r)

    def __call__(self, **values):
        if 'SearchableText' in values:
            st = values['SearchableText']
            if st.startswith('error'):
                raise ParseError
        return self.values()

    @property
    def _catalog(self):
        return self

    def getrid(self, value):
        return value in self and value or None
