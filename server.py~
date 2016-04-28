from twisted.web import server, resource
from twisted.internet import reactor
from restful import APIResource, GET, POST, PUT, DELETE, ALL
from utils import getIP

class SimpleRPC(APIResource):
    """A sample RPC RESTful server:
       * Two ways to bind a function to an URL
         - the resister function
         - @PUT('regex')"""

    def __init__(self):
        APIResource.__init__(self)
        self.register('GET', '^/regex/(?P<apid>[^/]+)$', self.GET_regex)
        
    def GET_regex(self, request, apid):
        self.preprocess(request)
        print 'regex is %s'% apid
        request.setResponseCode(400)
        return "regex is %s"%apid

    @GET('^/test')
    def GET_test(self, request):
        self.preprocess(request)
        ip = getIP(request)
        request.setResponseCode(200)
        return "request from ip %s" % ip

    @GET('^/getfishLocation')
    def GET_localtion(self,request):
#dsfsdfdsfds
        return "a lot of data"

    @ALL('^/')
    def default(self, request):
        self.preprocess(request)
        request.setResponseCode(200)
        return "Default RPC"

    def preprocess(self, request):
        ip = getIP(request)
        url = request.path
        print "request from %s to path %s" % (ip, url)

if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    site = server.Site(SimpleRPC())
    print "server is running"
    reactor.listenTCP(8080, site)
    reactor.run()
