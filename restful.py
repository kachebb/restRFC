from zope.interface.advice import addClassAdvisor
import re
from itertools import ifilter
from functools import wraps
from twisted.web.resource import Resource, NoResource

def method_factory_factory(method):
    def factory(regex):
        _f = {}
        def decorator(f):
            _f[f.__name__] = f
            return f
        def advisor(cls):
            def wrapped(f):
                def __init__(self, *args, **kwargs):
                    f(self, *args, **kwargs)
                    for func_name in _f:
                        orig = _f[func_name]
                        func = getattr(self, func_name)
                    if func.im_func==orig:
                        self.register(method, regex, func)
                return __init__
            cls.__init__ = wrapped(cls.__init__)
            return cls
        addClassAdvisor(advisor)
        return decorator
    return factory

ALL    = method_factory_factory('ALL')
GET    = method_factory_factory('GET')
POST   = method_factory_factory('POST')
PUT    = method_factory_factory('PUT')
DELETE = method_factory_factory('DELETE')

class _FakeResource(Resource):
    _result = ''
    isLeaf = True
    def __init__(self, result):
        Resource.__init__(self)
        self._result = result
    def render(self, request):
        return self._result


def maybeResource(f):
    @wraps(f)
    def inner(*args, **kwargs):
        result = f(*args, **kwargs)
        if not isinstance(result, Resource):
            result = _FakeResource(result)
        return result
    return inner


class APIResource(Resource):

    _registry = None

    def __init__(self, *args, **kwargs):
        Resource.__init__(self, *args, **kwargs)
        self._registry = []

    def _get_callback(self, request):
        filterf = lambda t:t[0] in (request.method, 'ALL')
        path_to_check = getattr(request, '_remaining_path', request.path)
        for m, r, cb in ifilter(filterf, self._registry):
            result = r.search(path_to_check)
            if result:
                request._remaining_path = path_to_check[result.span()[1]:]
                return cb, result.groupdict()
        return None, None

    def register(self, method, regex, callback):
        self._registry.append((method, re.compile(regex), callback))

    def unregister(self, method=None, regex=None, callback=None):
        if regex is not None: regex = re.compile(regex)
        for m, r, cb in self._registry[:]:
            if not method or (method and m==method):
                if not regex or (regex and r==regex):
                    if not callback or (callback and cb==callback):
                        self._registry.remove((m, r, cb))

    def getChild(self, name, request):
        r = self.children.get(name, None)
        if r is None:
            # Go into the thing
            callback, args = self._get_callback(request)
            if callback is None:
                return NoResource()
            else:
                return maybeResource(callback)(request, **args)
        else:
            return r


